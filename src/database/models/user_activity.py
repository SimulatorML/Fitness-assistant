from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import BaseModel

class UserActivity(BaseModel):
    """Модель активности пользователя."""
    __tablename__ = "user_activities"

    user_id = Column(Integer, ForeignKey("users.id"), comment="ID пользователя")
    activity_id = Column(Integer, ForeignKey("activities.id"), comment="ID активности")
    start_time = Column(DateTime, comment="Время начала активности")
    end_time = Column(DateTime, comment="Время окончания активности")
    duration = Column(Float, nullable=True, comment="Продолжительность активности (в минутах)")
    repetitions = Column(Integer, nullable=True, comment="Количество повторений (для силовых тренировок)")
    distance = Column(Float, nullable=True, comment="Пройденное расстояние (для бега)")

    user = relationship("User", back_populates="user_activities")
    activity = relationship("Activity", back_populates="user_activities")

    def __repr__(self):
        return f"<UserActivity(user_id={self.user_id}, activity_id={self.activity_id}, start_time={self.start_time}, end_time={self.end_time})>"