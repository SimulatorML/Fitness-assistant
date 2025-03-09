from datetime import datetime
from src.schemas.base import BaseDTO
from enum import Enum
from pydantic import validator
from typing import Optional, List

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"  # Малоподвижный образ жизни (офисная работа, нет спорта)
    LIGHT = "light"  # Лёгкая активность (какая-либо активность 1-2 раза в неделю, прогулки)
    MODERATE = "moderate"  # Умеренная активность (тренировки 3-4 раза в неделю)
    HIGH = "high"  # Высокая активность (интенсивные тренировки 5+ раз в неделю)
    ATHLETE = "athlete"  # Профессиональный уровень (спортсмен, тренировки 2 раза в день)

class Goal(str, Enum):
    fat_loss = "fat_loss"  # Сжигание жира
    muscle_gain = "muscle_gain"  # Набор мышечной массы
    maintenance = "maintenance"  # Поддержание формы
    endurance = "endurance"  # Развитие выносливости
    strength = "strength"  # Увеличение силы
    flexibility = "flexibility"  # Улучшение гибкости
    health = "health"  # Общее улучшение здоровья

class UserCreate(BaseDTO):
    telegram_id: int
    name: str
    height: int | None = None  # Сделали необязательными
    weight: int | None = None
    birth_date: datetime | None = None
    gender: str | None = None
    activity_level: ActivityLevel | None = None
    goal: Goal | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    health_restrictions: str | None = None
    preferred_activities: list[str] | None = None #В зависимости от хранения

    @validator("birth_date", pre=True)  # Валидатор для даты
    def parse_birth_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY")
        return value

class UserUpdate(BaseDTO):
    name: str | None = None
    height: int | None = None
    weight: int | None = None
    birth_date: datetime | None = None
    gender: str | None = None
    activity_level: ActivityLevel | None = None
    goal: Goal | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    health_restrictions: str | None = None
    preferred_activities: list[str] | None = None #В зависимости от хранения

    @validator("birth_date", pre=True)  # Валидатор для даты
    def parse_birth_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY")
        return value
class UserDTO(BaseDTO):
    id: int
    telegram_id: int
    name: str
    height: int | None = None
    weight: int | None = None
    birth_date: datetime | None = None
    gender: str | None = None
    activity_level: ActivityLevel | None = None
    goal: Goal | None = None
    created_at: datetime
    updated_at: datetime
    username: str | None = None  # Добавили
    first_name: str | None = None  # Добавили
    last_name: str | None = None  # Добавили
    health_restrictions: str | None = None  # Добавили
    preferred_activities: list[str] | None = None  # Добавили