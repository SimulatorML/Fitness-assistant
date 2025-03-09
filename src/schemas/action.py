from datetime import datetime
from src.schemas.base import BaseDTO
from enum import Enum
from typing import Optional

class ActionType(str, Enum):
    """User action types."""
    START = "start"  # Начало взаимодействия с ботом
    REGISTRATION = "registration"  # Регистрация пользователя
    HELP = "help"  # Запрос помощи/инструкции
    UPDATE_PROFILE = "update_profile" # Обновление профиля
    LOG_MEAL = "log_meal"  # Логирование еды
    LOG_ACTIVITY = "log_activity"  # Логирование активности
    MESSAGE = "message" #Для сообщений

class ActionCreate(BaseDTO):
    """Schema for logging user actions."""
    action_type: ActionType
    content: str | None = None
    response: str | None = None
    user_id: int

class Action(BaseDTO):
    """Schema for logging user actions."""
    id: int  # Добавили
    timestamp: datetime  # Изменили
    user_id: int
    action_type: ActionType
    content: str | None = None  # Добавили
    response: str | None = None  # Добавили