from sqlalchemy import Column, Integer, String
from src.database.models.base import Base


__all__ = ["User"]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    activity_level = Column(String, nullable=False)
    goal = Column(String, nullable=False)
