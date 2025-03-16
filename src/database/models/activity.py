from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from src.database.models.base import Base


__all__ = ["Activity"]


class Activity(Base):
    """Schema for logging user activities."""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    activity_type = Column(String, nullable=False)
