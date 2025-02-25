from sqlalchemy import Column, Integer, DateTime
from src.database.models.base import Base


__all__ = ["Action"]


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime)
    