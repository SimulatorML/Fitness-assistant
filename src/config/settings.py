from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


load_dotenv()  # Загружаем переменные окружения из файла .env

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn = Field(..., env="DATABASE_URL")
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    GOOGLE_API_KEY: str = Field(..., env="GOOGLE_API_KEY")
    API_URL: str = Field("http://localhost:8000", env="API_URL")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# Создаём экземпляр настроек
settings = Settings()
print("Settings loaded:", settings)