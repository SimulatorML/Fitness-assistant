from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connection import session_maker


__all__ = ["DBSession"]


async def _create_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(dependency=_create_database_session)]
