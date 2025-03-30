import pytest
from httpx import AsyncClient
from api.app import get_application


@pytest.mark.asyncio
async def test_redis_ping():
    app = get_application()
    async with AsyncClient(app=app, base_url="http://test") as client:
        res = await client.get("/redis/ping")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "OK"
        assert data["ping"] == "pong"
