# tests/conftest.py

import pytest_asyncio
from api.app import get_application
from httpx import AsyncClient
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connection import session_maker
from dotenv import load_dotenv

load_dotenv() 


@pytest_asyncio.fixture
async def app():
    return get_application()


@pytest_asyncio.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with session_maker() as session:
        yield session
        await session.rollback()
