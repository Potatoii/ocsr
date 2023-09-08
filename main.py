import os
import uuid

import aiofiles
import uvicorn
from fastapi import FastAPI, UploadFile

import ocsr_utils
from commons.log_utils import logger
from commons.middlewares import BaseRequest
from commons.schemas import Result, OcsrModel
from config import settings

app = FastAPI(
    title="DECIMER API"
)
app.add_middleware(BaseRequest)


@app.post("/upload", response_model=Result)
async def upload_file(file: UploadFile):
    content_type = file.content_type
    logger.info(f"File Content Type: {content_type}")
    key = uuid.uuid4().hex
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    async with aiofiles.open(f"tmp/{key}.{file.filename.split('.')[-1]}", "wb") as f:
        await f.write(await file.read())
    if content_type.startswith("image/"):
        file_info = f"{key}.{file.filename.split('.')[-1]}|image"
    elif content_type == "application/pdf":
        file_info = f"{key}.{file.filename.split('.')[-1]}|pdf"
    else:
        raise ValueError(f"File Content Type: {content_type} is not supported.")
    return Result(data={"file_info": file_info})


@app.post("/ocsr", response_model=Result)
async def ocsr(
        ocsr_params: OcsrModel,
):
    html_url = await ocsr_utils.ocsr_analysis(ocsr_params.file_info)
    return Result(data={"html_url": html_url})


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, access_log=False)
