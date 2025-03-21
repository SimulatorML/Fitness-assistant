from datetime import datetime
from src.schemas.base import BaseDTO
from enum import Enum


class ActionType(str, Enum):
    """User action types."""
    START = "start"  # Начало взаимодействия с ботом
    REGISTRATION = "registration"  # Регистрация пользователя после завершения онбоардинга
    HELP = "help"  # Запрос помощи/инструкции
    UPDATE_PROFILE = "update_profile" # Обновление профиля пользователя
    LOG_MEAL = "log_meal"  # Логирование еды
    LOG_ACTIVITY = "log_activity"  # Логирование активности


class Action(BaseDTO):
    """Schema for logging user actions."""
    time: datetime
    user_id: int
    action_type: ActionType
