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

class UserCreate(BaseDTO):
    telegram_id: int
    name: str
    height: int
    weight: int
    age: int
    gender: str
    activity_level: ActivityLevel
    goal: Goal

class UserUpdate(BaseDTO):
    name: str | None = None
    height: int | None = None
    weight: int | None = None
    age: int | None = None
    gender: str | None = None
    activity_level: ActivityLevel | None = None
    goal: Goal | None = None

class UserDTO(BaseDTO):
    id: int
    telegram_id: int
    name: str
    height: int
    weight: int
    age: int
    gender: str
    activity_level: ActivityLevel
    goal: Goal
