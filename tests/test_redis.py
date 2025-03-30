import pytest
from httpx import AsyncClient
from api.app import get_application
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_redis_ping():
    app = get_application()

    # Create a FastAPI test client just to run startup/shutdown events
    with TestClient(app):
        async with AsyncClient(base_url="http://test", app=app) as client:
            res = await client.get("/api/v1/redis/ping")
            assert res.status_code == 200
            data = res.json()
            assert data["status"] == "OK"
            assert data["ping"] == "pong"
