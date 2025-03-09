from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import models
from src.schemas.activity import ActivityCreate, ActivityUpdate, ActivityDTO  # Импортируем схемы напрямую
from typing import List, Optional

async def create_activity(db: AsyncSession, activity: ActivityCreate) -> models.Activity:  # Изменили тип activity
    """Создает новую активность в базе данных."""
    try:
        db_activity = models.Activity(**activity.dict())
        db.add(db_activity)
        await db.commit()
        await db.refresh(db_activity)
        return db_activity
    except Exception as e:
        await db.rollback()
        raise e

async def get_activity_by_id(db: AsyncSession, activity_id: int) -> Optional[models.Activity]:
    """Возвращает активность по ID или None, если активность не найдена."""
    result = await db.execute(select(models.Activity).where(models.Activity.id == activity_id))
    return result.scalar_one_or_none()

async def get_all_activities(db: AsyncSession) -> List[models.Activity]:
    """Возвращает список всех активностей."""
    result = await db.execute(select(models.Activity))
    return result.scalars().all()

async def update_activity(db: AsyncSession, activity: ActivityUpdate, activity_id: int) -> Optional[models.Activity]:  # Изменили тип activity
    """Обновляет данные активности по ID. Возвращает обновленную активность или None."""
    db_activity = await db.get(models.Activity, activity_id)
    if db_activity:
        try:
            for key, value in activity.dict(exclude_unset=True).items():
                setattr(db_activity, key, value)
            db.add(db_activity)
            await db.commit()
            await db.refresh(db_activity)
            return db_activity
        except Exception as e:
            await db.rollback()
            raise e
    return None

async def delete_activity(db: AsyncSession, activity_id: int) -> Optional[models.Activity]:
    """Удаляет активность по ID. Возвращает удаленную активность или None."""
    db_activity = await db.get(models.Activity, activity_id)
    if db_activity:
        try:
            await db.delete(db_activity)
            await db.commit()
            return db_activity
        except Exception as e:
            await db.rollback()
            raise e
    return None