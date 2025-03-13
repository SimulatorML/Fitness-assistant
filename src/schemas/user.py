from datetime import datetime
from src.schemas.base import BaseDTO
from enum import Enum


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

class InterfaceLanguage(str, Enum):
    ENGLISH = "english"
    RUSSIAN = "russian"

class UserCreate(BaseDTO):
    telegram_id: int
    name: str
    height: int
    weight: float
    birth_date: datetime
    gender: str
    activity_level: ActivityLevel
    goal: Goal
    health_restrictions: str | None = None
    preferred_activities: str | None = None

class UserUpdate(BaseDTO):
    name: str | None = None
    height: int | None = None
    weight: float | None = None
    birth_date: datetime | None = None
    gender: str | None = None
    activity_level: ActivityLevel | None = None
    goal: Goal | None = None
    health_restrictions: str | None = None
    preferred_activities: str | None = None

class UserDTO(BaseDTO):
    id: int
    telegram_id: int
    name: str
    height: int
    weight: float
    birth_date: datetime
    gender: str
    activity_level: ActivityLevel
    goal: Goal
    health_restrictions: str | None = None
    preferred_activities: str | None = None
    created_at: datetime
    updated_at: datetime
