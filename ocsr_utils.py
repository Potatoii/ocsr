import asyncio
import base64
import io
import os

import aiofiles
import cv2
import numpy as np
from PIL import Image
from jinja2 import Environment, FileSystemLoader
from pdf2image import convert_from_bytes
from rdkit import Chem
from rdkit.Chem import Draw

from commons.log_utils import logger
from segmentation import segment_chemical_structures
from transformer import predict_smiles

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("ocsr.html")


def mol_to_image(mol, size=(500, 500), kekulize=True) -> io.BytesIO:
    """
    先对分子进行克库勒化，然后计算其2D坐标，然后通过MolDraw2DCairo绘制分子。
    最后，获取 Cairo Drawer 的内容并转换为 PIL Image 来显示。
    """
    mc = Chem.Mol(mol.ToBinary())
    if kekulize:
        try:
            Chem.Kekulize(mc)
        except:
            mc = Chem.Mol(mol.ToBinary())
    if not mc.GetNumConformers():
        Chem.rdDepictor.Compute2DCoords(mc)
    drawer = Draw.MolDraw2DCairo(*size)
    drawer.DrawMolecule(mc)
    drawer.FinishDrawing()
    rdkit_img_io = io.BytesIO(drawer.GetDrawingText())
    return rdkit_img_io


async def ocsr_analysis(file_info: str):
    file_name, file_type = file_info.split("|")
    tmp_file = f"tmp/{file_name}"
    if file_type == "image":
        pages = [cv2.imread(tmp_file)]
    elif file_type == "pdf":
        async with aiofiles.open(f"{tmp_file}", "rb") as f:
            pages = convert_from_bytes(await f.read())
    else:
        raise ValueError(f"File Type: {file_type} is not supported.")
    os.remove(tmp_file)
    final_data = []
    for page_number, page_image in enumerate(pages):
        logger.info(f"Get Segment Images From Page {page_number + 1}...")
        segments = await asyncio.to_thread(segment_chemical_structures, np.array(page_image), True, False)
        logger.info(f"{len(segments)} Segment Images From Page {page_number + 1}.")
        for i, segment_image_array in enumerate(segments):
            segment_image = Image.fromarray(segment_image_array)
            segment_img_io = io.BytesIO()
            segment_image.save(segment_img_io, "PNG")
            segment_img_io.seek(0)
            smiles = await asyncio.to_thread(predict_smiles, segment_image)
            mol = Chem.MolFromSmiles(smiles)  # noqa
            if not mol:
                continue
            rdkit_img_io = mol_to_image(mol)
            final_data.append(
                (
                    base64.b64encode(segment_img_io.getvalue()).decode(),
                    base64.b64encode(rdkit_img_io.getvalue()).decode(),
                    smiles,
                )
            )
    output = template.render(data=final_data)
    html_path = f"tmp/{file_name.split('.')[0]}.html"
    async with aiofiles.open(html_path, "w") as f:
        await f.write(output)
    return html_path
