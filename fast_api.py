import asyncio
from typing import Dict, List, Any

import fastapi
import httpx
from fastapi import Request
from pydantic import BaseModel

api = fastapi.FastAPI()


class UrlModel(BaseModel):
    url: str
    query: str


class RequestModel(BaseModel):
    urls: List[UrlModel]
    max_timeout: str


async def parse_url(client, time_out, url, query, ):
    res_dict = {'url': url, 'status': 'error'}

    try:
        response = await client.get(url, timeout=time_out)
    except Exception as error:
        print(error.__class__, error)
        return res_dict
    else:
        status = response.status_code

    if status == 200:
        cnt = response.text.count(query)
        res_dict['status'] = 'ok'
        res_dict['count'] = cnt
        return res_dict

    return res_dict


async def fetch_all_urls(urls, time_out: float) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        task_list = [
            parse_url(client, time_out, item['url'], item['query'])
            for item in
            urls
        ]
        return await asyncio.gather(*task_list)


@api.post('/counts')
async def weather(request: Request):

    data = await request.json()
    time_out = int(data['max_timeout']) / 1000
    urls = data['urls']

    result = await fetch_all_urls(urls, time_out)

    return {'urls': result}
