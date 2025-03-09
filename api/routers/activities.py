# app/activities.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connection import get_db
from src.database.models import Activity
from src.schemas.activity import ActivityCreate, ActivityUpdate, ActivityDTO
from src.services import activity_service


router = APIRouter(prefix="/activities", tags=["activities"])

@router.post("/", response_model=ActivityDTO)
async def create_new_activity(activity: ActivityCreate, db: AsyncSession = Depends(get_db)):
    """Создание новой активности."""
    return await create_activity(db, activity)

@router.get("/{activity_id}", response_model=ActivityDTO)
async def read_activity(activity_id: int, db: AsyncSession = Depends(get_db)):
    """Получение активности по ID."""
    activity_from_db = await get_activity_by_id(db, activity_id)
    if activity_from_db is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity_from_db

@router.get("/", response_model=list[ActivityDTO])
async def read_all_activities(db: AsyncSession = Depends(get_db)):
    """Получение списка всех активностей."""
    return await get_all_activities(db)

@router.put("/{activity_id}", response_model=ActivityDTO)
async def update_existing_activity(activity_id: int, activity: ActivityUpdate, db: AsyncSession = Depends(get_db)):
    """Обновление активности по ID."""
    updated_activity = await update_activity(db, activity, activity_id)
    if updated_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated_activity

@router.delete("/{activity_id}", response_model=ActivityDTO)
async def delete_existing_activity(activity_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление активности по ID."""
    deleted_activity = await delete_activity(db, activity_id)
    if deleted_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return deleted_activity