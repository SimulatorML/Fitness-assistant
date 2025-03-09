# bot/__main__.py
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from sqlalchemy import text
from aiogram.client.bot import Bot, DefaultBotProperties


from bot import handlers
from src.database.connection import engine
from src.config.settings import settings


# Настройка логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Инициализация бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

async def init_db():
    """Проверяет подключение к базе данных."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful.")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise  # Остановит выполнение, если БД недоступна

async def main():
    """Запускает бота."""
    # Подключаем роутеры
    dp.include_router(handlers.common_router)
    dp.include_router(handlers.fitness_router)

    # Проверяем БД
    await init_db()

    # Запускаем бота
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()  # Закрываем сессию бота

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
    except Exception as e:
        logger.exception("An unexpected error occurred: %s", e)