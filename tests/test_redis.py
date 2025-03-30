import pytest
from httpx import AsyncClient, ASGITransport


@pytest.mark.asyncio
async def test_redis_ping(app_with_redis):
    transport = ASGITransport(app=app_with_redis)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/redis/ping")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "OK"
        assert data["ping"] == "pong"

