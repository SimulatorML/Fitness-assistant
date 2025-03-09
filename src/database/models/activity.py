from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import BaseModel  

class Activity(BaseModel):
    """Модель активности."""
    __tablename__ = "activities"

    name = Column(String, nullable=False, comment="Название активности (например, бег, плавание, йога)")
    description = Column(Text, nullable=True, comment="Описание активности")
    type = Column(String, nullable=True, comment="Тип активности (например, кардио, силовая тренировка)")

    user_activities = relationship("UserActivity", back_populates="activity")

    def __repr__(self):
        return f"<Activity(id={self.id}, name='{self.name}')>"