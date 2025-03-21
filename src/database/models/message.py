from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func
from datetime import datetime
from src.database.models.base import Base


__all__ = ["Message"]


class Message(Base): 
    """Schema to store long-term conversation history"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)