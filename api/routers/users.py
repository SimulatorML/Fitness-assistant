from fastapi import APIRouter, HTTPException, Depends
from src.database.models import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connection import get_db
from src.schemas.user import UserDTO, UserCreate, UserUpdate
from sqlalchemy import select
import logging
from src.config.settings import settings  # Добавили импорт settings

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int, session: AsyncSession = Depends(lambda: get_db(settings))) -> UserDTO:
    """Get user info from database"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDTO.model_validate(user)

@router.get("/by_telegram/{telegram_id}", response_model=UserDTO)
async def get_user_by_telegram_id(telegram_id: int, session: AsyncSession = Depends(lambda: get_db(settings))) -> UserDTO:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDTO.model_validate(user)

@router.post("/", response_model=UserDTO)
async def create_user(user: UserCreate, session: AsyncSession = Depends(lambda: get_db(settings))) -> UserDTO:
    """Create a new user in database"""
    existing_user = await session.execute(select(User).where(User.telegram_id == user.telegram_id))
    existing_user = existing_user.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this telegram_id already exists")

    new_user = User(**user.model_dump())
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {e}") from e
    return UserDTO.model_validate(new_user)

@router.put("/{user_id}", response_model=UserDTO)
async def update_user(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(lambda: get_db(settings))) -> UserDTO:
    """Обновить пользователя в БД."""
    user = await session.get(User, user_id)
    if user is None:
        logging.warning(f"❌ User {user_id} not found for update")
        raise HTTPException(status_code=404, detail="User not found")

    updated_data = user_update.model_dump(exclude_unset=True)
    if updated_data:
        await session.execute(
            User.__table__.update().where(User.id == user_id).values(**updated_data)
        )

    try:
        await session.commit()
        await session.refresh(user)
        logging.info(f"✅ User {user_id} updated successfully")
    except IntegrityError as e:
        await session.rollback()
        logging.error(f"❌ Error updating user {user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail="Problem with updating user information") from e

    return UserDTO.model_validate(user)

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, session: AsyncSession = Depends(lambda: get_db(settings))) -> None:
    """Мягкое удаление пользователя."""
    user = await session.get(User, user_id)
    if user is None:
        logging.warning(f"❌ User {user_id} not found for deletion")
        raise HTTPException(status_code=404, detail="User not found")

    user.is_deleted = True
    try:
        await session.commit()
        logging.info(f"🗑️ User {user_id} marked as deleted")
    except Exception as e:
        await session.rollback()
        logging.error(f"❌ Error deleting user {user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error") from e