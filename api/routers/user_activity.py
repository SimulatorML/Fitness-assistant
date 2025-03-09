# src/views/user_activity.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connection import get_db
from src.schemas.user_activity import UserActivityCreate, UserActivityDTO
from src.services.user_activity_service import (
    create_user_activity,
    get_user_activity_by_id,
    get_all_user_activities,
    delete_user_activity
)

router = APIRouter(prefix="/user_activities", tags=["user_activities"])

@router.post("/", response_model=UserActivityDTO)
async def create_new_user_activity(user_activity: UserActivityCreate, db: AsyncSession = Depends(get_db)):
    """Создание новой связи пользователь-активность."""
    return await create_user_activity(db, user_activity)

@router.get("/{user_activity_id}", response_model=UserActivityDTO)
async def read_user_activity(user_activity_id: int, db: AsyncSession = Depends(get_db)):
    """Получение связи пользователь-активность по ID."""
    user_activity_from_db = await get_user_activity_by_id(db, user_activity_id)
    if user_activity_from_db is None:
        raise HTTPException(status_code=404, detail="User Activity not found")
    return user_activity_from_db

@router.get("/", response_model=list[UserActivityDTO])
async def read_all_user_activities(db: AsyncSession = Depends(get_db)):
    """Получение списка всех связей пользователь-активность."""
    return await get_all_user_activities(db)

@router.delete("/{user_activity_id}", response_model=UserActivityDTO)
async def delete_existing_user_activity(user_activity_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление связи пользователь-активность по ID."""
    deleted_user_activity = await delete_user_activity(db, user_activity_id)
    if deleted_user_activity is None:
        raise HTTPException(status_code=404, detail="User Activity not found")
    return deleted_user_activity