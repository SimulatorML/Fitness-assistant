from sqlalchemy import Column, Date, DateTime, Float, Integer, String, func
from src.database.models.base import Base


__all__ = ["User"]


class User(Base):
    """User profile schema."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    activity_level = Column(String, nullable=False)
    goal = Column(String, nullable=False)
    health_restrictions = Column(String, nullable=True)
    preferred_activities = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
