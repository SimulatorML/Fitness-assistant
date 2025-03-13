from sqlalchemy import Column, Integer
from src.database.models.base import Base


__all__ = ["Activity"]


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    