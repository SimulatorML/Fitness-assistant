import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from api.app import get_application
from asgi_lifespan import LifespanManager


import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from asgi_lifespan import LifespanManager
from api.app import get_application


@pytest.mark.asyncio
async def test_redis_ping():
    app = get_application()

    async with LifespanManager(app):
        with TestClient(app) as sync_client:
            async with AsyncClient(base_url="http://test", transport=sync_client._transport) as client:
                res = await client.get("/api/v1/redis/ping")
                assert res.status_code == 200
                data = res.json()
                assert data["status"] == "OK"
                assert data["ping"] == "pong"