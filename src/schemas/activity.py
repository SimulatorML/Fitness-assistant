from src.schemas.base import BaseDTO
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ActivityCreate(BaseDTO):
    """Схема для создания активности."""
    name: str
    description: Optional[str] = None
    type: Optional[str] = None


class ActivityUpdate(BaseDTO):
    """Схема для обновления активности."""
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None


class ActivityDTO(BaseDTO):
    """Схема для передачи данных активности."""
    id: int
    name: str
    description: Optional[str] = None
    type: Optional[str] = None