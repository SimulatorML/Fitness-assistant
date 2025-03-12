from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from src.database.models.base import Base


__all__ = ["Action"]


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime)
    user_id = ForeignKey("users.id")
    action_type = Column(String, nullable=False)
