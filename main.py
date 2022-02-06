from typing import List, Dict

import fastapi

from schemas import DataModel, UrlModel
from utils import fetch_all_urls

app = fastapi.FastAPI()


@app.post('/counts')
async def counts(data: DataModel):
    time_out: float = data.max_timeout / 1000
    urls: List[UrlModel] = data.urls

    result: List[Dict] = await fetch_all_urls(urls, time_out)

    return {'urls': result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
