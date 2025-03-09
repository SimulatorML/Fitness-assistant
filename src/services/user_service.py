from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import models
from src.schemas.user import UserCreate, UserDTO, UserUpdate  # Импортируем схемы напрямую
from typing import List, Optional
from datetime import datetime

async def create_user(db: AsyncSession, user: UserCreate) -> models.User: # Изменили тип user
    """Создает нового пользователя в базе данных."""
    try:
        user_dict = user.dict()
        user_dict["birth_date"] = datetime.strptime(user_dict["birth_date"], '%d.%m.%Y').date()
        db_user = models.User(**user_dict)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        await db.rollback()
        raise e

async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> Optional[models.User]:
    """Возвращает пользователя по telegram_id или None, если пользователь не найден."""
    result = await db.execute(select(models.User).where(models.User.telegram_id == telegram_id))
    return result.scalar_one_or_none()

async def get_all_users(db: AsyncSession) -> List[models.User]:
    """Возвращает список всех пользователей."""
    result = await db.execute(select(models.User))
    return result.scalars().all()

async def update_user(db: AsyncSession, user: UserUpdate, user_id: int) -> Optional[models.User]: # Изменили тип user
    """Обновляет данные пользователя по id. Возвращает обновленного пользователя или None."""
    db_user = await db.get(models.User, user_id)
    if db_user:
        try:
            for key, value in user.dict(exclude_unset=True).items():
                if key == "birth_date" and value is not None:
                    setattr(db_user, key, datetime.strptime(value, '%d.%m.%Y').date())
                else:
                    setattr(db_user, key, value)
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except Exception as e:
            await db.rollback()
            raise e
    return None

async def delete_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
    """Удаляет пользователя по id. Возвращает удаленного пользователя или None."""
    db_user = await db.get(models.User, user_id)
    if db_user:
        try:
            await db.delete(db_user)
            await db.commit()
            return db_user
        except Exception as e:
            await db.rollback()
            raise e
    return None