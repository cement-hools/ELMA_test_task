from typing import List

from pydantic import BaseModel, PositiveInt


class UrlModel(BaseModel):
    url: str
    query: str


class DataModel(BaseModel):
    urls: List[UrlModel]
    max_timeout: PositiveInt = 3000
