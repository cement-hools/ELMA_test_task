import asyncio

import pytest as pytest
from httpx import AsyncClient, ConnectError, TimeoutException

from main import app
from utils import parse_url


@pytest.mark.asyncio
class TestCounts:
    """Тест endpoint '/counts'."""

    async def test_counts_valid(self):
        """Тест с валидными данными."""
        data = {
            "urls": [
                {"url": "https://python.org", "query": "python"},
                {"url": "https://www.djangoproject.com", "query": "django"},
                {"url": "https://варвар.com", "query": "python"},
                {"url": "https://pythonist.ru", "query": 2}
            ],
            "max_timeout": "3000"
        }
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/counts", json=data)
        assert response.status_code == 200
        assert "urls" in response.json()
        urls_list = response.json().get("urls")
        assert isinstance(urls_list, list) is True
        assert len(urls_list) == len(data["urls"])

    async def test_counts_not_required(self):
        """Нет обязательно поля."""
        data = {
            "list": [
                {"url": "https://python.org", "query": "python"},
                {"url": "https://www.djangoproject.com", "query": "django"},
                {"url": "https://варвар.com", "query": "python"},
                {"url": "https://pythonist.ru", "query": 2}
            ],
            "max_timeout": "3000"
        }
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/counts", json=data)
        assert response.status_code == 422
        assert "urls" not in response.json()
        assert "detail" in response.json()
        assert response.json()["detail"][0].get("msg") == "field required"
        assert "urls" in response.json()["detail"][0].get("loc")

    async def test_counts_non_max_timeout(self):
        """Нет max_timeout."""
        data = {
            "urls": [
                {"url": "https://python.org", "query": "python"},
                {"url": "https://www.djangoproject.com", "query": "django"},
                {"url": "https://варвар.com", "query": "python"},
                {"url": "https://pythonist.ru", "query": 2}
            ]
        }
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/counts", json=data)
        assert response.status_code == 200
        assert "urls" in response.json()
        urls_list = response.json().get("urls")
        assert isinstance(urls_list, list) is True
        assert len(urls_list) == len(data["urls"])

    async def test_counts_invalid_max_timeout(self):
        """Не валидное значение max_timeout."""
        data = {
            "urls": [
                {"url": "https://python.org", "query": "python"},
                {"url": "https://www.djangoproject.com", "query": "django"},
                {"url": "https://варвар.com", "query": "python"},
                {"url": "https://pythonist.ru", "query": 2}
            ],
            "max_timeout": "test"
        }
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/counts", json=data)
        assert response.status_code == 422
        assert "detail" in response.json()
        assert response.json()["detail"][0].get("msg") == "value is not a valid integer"
        assert "max_timeout" in response.json()["detail"][0].get("loc")

    async def test_counts_negative_max_timeout(self):
        """Отрицательный max_timeout."""
        data = {
            "urls": [
                {"url": "https://python.org", "query": "python"},
                {"url": "https://www.djangoproject.com", "query": "django"},
                {"url": "https://варвар.com", "query": "python"},
                {"url": "https://pythonist.ru", "query": 2}
            ],
            "max_timeout": -3000
        }
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/counts", json=data)
        assert response.status_code == 422
        assert "detail" in response.json()
        greater_message = "ensure this value is greater than 0"
        assert response.json()["detail"][0].get("msg") == greater_message
        assert "max_timeout" in response.json()["detail"][0].get("loc")


@pytest.mark.asyncio
class TestParseUrl:
    """Тест функции parse_url."""

    async def test_parse_url_valid(self, httpx_mock):
        """Работает с верным адресом."""
        url = "https://www.python.com"
        query = "o"
        text = "foooo"

        httpx_mock.add_response(text=text)
        # httpx_mock.add_exception(Exception)
        async with AsyncClient() as client:
            res = await asyncio.gather(parse_url(client, 2, url, query))

        assert isinstance(res, list) is True
        result = res[0]
        assert isinstance(result, dict) is True
        assert "url" in result
        assert result["url"] == url
        assert "status" in result
        assert result["status"] == "ok"
        assert "count" in result
        assert result["count"] == 4

    async def test_parse_url_invalid(self, httpx_mock):
        """Работает с не валидным адресом."""
        url = "https://ww@.-5644.com"
        query = "o"
        text = "foooo"

        httpx_mock.add_exception(ConnectError)
        async with AsyncClient() as client:
            res = await asyncio.gather(parse_url(client, 2, url, query))

        assert isinstance(res, list) is True
        result = res[0]
        assert isinstance(result, dict) is True
        assert "url" in result
        assert result["url"] == url
        assert "status" in result
        assert result["status"] == "error"
        assert "count" not in result

    async def test_parse_url_timeout(self, httpx_mock):
        """Превышен таймаут запроса."""
        url = "https://www.python.com"
        query = "o"

        httpx_mock.add_exception(TimeoutException)
        async with AsyncClient() as client:
            res = await asyncio.gather(parse_url(client, 1, url, query))

        assert isinstance(res, list) is True
        result = res[0]
        assert isinstance(result, dict) is True
        assert "url" in result
        assert result["url"] == url
        assert "status" in result
        assert result["status"] == "error"
        assert "count" not in result

    async def test_parse_url_invalid_status(self, httpx_mock):
        """Статус ответа не 200."""
        url = "https://python.com"
        query = "o"

        httpx_mock.add_response(status_code=301)
        async with AsyncClient() as client:
            res = await asyncio.gather(parse_url(client, 2, url, query))

        assert isinstance(res, list) is True
        result = res[0]
        assert isinstance(result, dict) is True
        assert "url" in result
        assert result["url"] == url
        assert "status" in result
        assert result["status"] == "error"
        assert "count" not in result
