from sqlalchemy import Column, ForeignKey, Integer, DateTime, String
from src.database.models.base import Base


__all__ = ["Action"]


class Action(Base):
    """Schema for logging user actions in telegram bot."""
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action_type = Column(String, nullable=False)
