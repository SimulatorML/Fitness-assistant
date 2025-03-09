# src/schemas/user_activity.py
from src.schemas.base import BaseDTO
from datetime import datetime
from typing import Optional

class UserActivityCreate(BaseDTO):
        """Схема для создания связи пользователь-активность."""
        user_id: int
        activity_id: int
        start_time: datetime
        end_time: datetime
        duration: Optional[float] = None
        repetitions: Optional[int] = None
        distance: Optional[float] = None

class UserActivityDTO(BaseDTO):
        """Схема для передачи данных связи пользователь-активность."""
        id: int
        user_id: int
        activity_id: int
        start_time: datetime
        end_time: datetime
        duration: Optional[float] = None
        repetitions: Optional[int] = None
        distance: Optional[float] = None