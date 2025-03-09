from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, Text, func
from sqlalchemy.orm import relationship
from .base import BaseModel  

class Action(BaseModel):
    """Модель действия пользователя."""
    __tablename__ = "actions"

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True, comment="Время выполнения действия")
    user_id = Column(Integer, ForeignKey("users.id"), index=True, comment="ID пользователя")
    user = relationship("User", back_populates="actions")
    action_type = Column(String, nullable=False, comment="Тип действия (например, запрос к LLM, ввод данных)")
    content = Column(Text, nullable=True, comment="Содержание действия (например, запрос пользователя)")
    response = Column(Text, nullable=True, comment="Ответ на действие (например, ответ LLM)")

    def __repr__(self):
        return f"<Action(id={self.id}, user_id={self.user_id}, type='{self.action_type}', timestamp={self.timestamp})>"