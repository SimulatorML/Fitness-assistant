from src.schemas.base import BaseDTO


class UserCreate(BaseDTO):
    name: str


class UserUpdate(BaseDTO):
    name: str


class UserDTO(BaseDTO):
    id: int
