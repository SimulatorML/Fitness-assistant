from sqlalchemy import Column, Integer
from src.database.models.base import Base


__all__ = ["User"]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

