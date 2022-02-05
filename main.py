import fastapi

from schemas import DataModel
from utils import fetch_all_urls

api = fastapi.FastAPI()


@api.post('/counts')
async def counts(data: DataModel):
    time_out = data.max_timeout / 1000
    urls = data.urls

    result = await fetch_all_urls(urls, time_out)

    return {'urls': result}
