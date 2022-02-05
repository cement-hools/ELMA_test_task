from typing import List

from pydantic import BaseModel


class UrlModel(BaseModel):
    url: str
    query: str


class DataModel(BaseModel):
    urls: List[UrlModel]
    max_timeout: int = 3000
