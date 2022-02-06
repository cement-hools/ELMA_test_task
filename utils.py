import asyncio
import logging
from typing import Dict, Union, List

from httpx import AsyncClient

from schemas import UrlModel

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    ),
)
logger = logging.getLogger(__name__)


async def parse_url(
        client: AsyncClient, time_out: float, url: str, query: str
) -> Dict[str, Union[str, int]]:
    res_dict = {'url': url, 'status': 'error'}

    try:
        response = await client.get(url, timeout=time_out)
    except Exception as error:
        logger.error(f"{url}: {error.__class__.__name__}, {error}")
        return res_dict
    else:
        status = response.status_code

    if status == 200:
        cnt = response.text.count(query)
        res_dict['status'] = 'ok'
        res_dict['count'] = cnt
        return res_dict

    return res_dict


async def fetch_all_urls(urls: List[UrlModel], time_out: float):
    async with AsyncClient() as client:
        task_list = [
            parse_url(client, time_out, item.url, item.query)
            for item in urls
        ]
        return await asyncio.gather(*task_list)
