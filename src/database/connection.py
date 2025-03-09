from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config.settings import settings
from typing import AsyncGenerator

# Создаем движок для асинхронного взаимодействия с базой данных
engine = create_async_engine(str(settings.DATABASE_URL), echo=False)


# Создаем фабрику сессий
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Функция для получения сессии БД
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# Функция закрытия соединения с БД (при необходимости)
async def close_db():
    await engine.dispose()
