# src/database/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel  # Изменено наследование

class User(BaseModel):  # Изменено наследование
    """Модель пользователя."""
    __tablename__ = "users"

    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False, comment="Telegram ID пользователя")
    username = Column(String, index=True, nullable=True, comment="Имя пользователя в Telegram") #Убрали unique
    first_name = Column(String, nullable=True, index=True, comment="Имя пользователя") #Добавили index
    # last_name = Column(String, nullable=True, index=True, comment="Фамилия пользователя") #Убрали
    name = Column(String, nullable=False, comment="Отображаемое имя пользователя")
    birth_date = Column(Date, nullable=True, comment="Дата рождения")
    gender = Column(String, nullable=True, comment="Пол")
    height = Column(Integer, nullable=True, comment="Рост в сантиметрах")
    weight = Column(Integer, nullable=True, comment="Вес в килограммах")
    activity_level = Column(String, nullable=True, comment="Уровень активности")
    goal = Column(String, nullable=True, comment="Цель пользователя (например, похудение, набор массы)")
    health_restrictions = Column(String, nullable=True, comment="Медицинские ограничения")
    # preferred_activities = Column(String, nullable=True)  # Убрали
    
    actions = relationship("Action", back_populates="user")
    user_activities = relationship("UserActivity", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.username}')>"