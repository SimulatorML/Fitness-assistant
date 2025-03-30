from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, func
from src.database.models.base import Base

__all__ = ["SubSummary"]

class SubSummary(Base):
    __tablename__ = "sub_summaries"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=False, index=True)
    summary = Column(String, nullable=False)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
