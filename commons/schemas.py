from typing import Any

from pydantic import BaseModel


class Result(BaseModel):
    code: int = 0
    msg: str = "success"
    data: Any = {}


class OcsrModel(BaseModel):
    file_info: str