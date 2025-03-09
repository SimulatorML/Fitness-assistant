import logging
from fastapi import FastAPI
from api.routers import router
from src.database.connection import close_db, engine
from src.database.models import Base
from sqlalchemy import text
from api.routers import router


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Инициализация FastAPI приложения
app = FastAPI(title="Fitness Assistant API", version="1.0")

# Подключение маршрутов
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Функция запуска, проверяет соединение с БД и создаёт таблицы."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logging.info("✅ Database connection successful.")

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logging.info("✅ Database tables created successfully.")

    except Exception as e:
        logging.error(f"❌ Database connection failed: {e}", exc_info=True)

@app.on_event("shutdown")
async def shutdown_event():
    """Функция завершения, закрывает соединение с БД."""
    await close_db()
    logging.info("🔄 Database connection closed.")

@app.get("/", tags=["Health Check"])
async def root():
    """Корневой эндпоинт для проверки состояния API."""
    return {"message": "🚀 Fitness Assistant API is running!"}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
