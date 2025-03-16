from sqlalchemy import Column, ForeignKey, Integer, String
from src.database.models.base import Base


__all__ = ["Program"]


class Program(Base):
    """Schema for training programs generated by LLM."""
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    program = Column(String, nullable=False)
    model = Column(String, nullable=False)  # LLM model name
