import pytest
from httpx import AsyncClient, ASGITransport
from api.app import get_application


@pytest.mark.asyncio
async def test_redis_ping():
    app = get_application()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # manually trigger Redis startup
        await app.router.startup()
        
        res = await client.get("/api/v1/redis/ping")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "OK"
        assert data["ping"] == "pong"

        # manually trigger Redis shutdown
        await app.router.shutdown()
