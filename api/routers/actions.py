# src/views/action.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connection import get_db
from src.schemas.action import ActionCreate, ActionDTO
from src.services.action_service import (
    create_action,
    get_action_by_id,
    get_all_actions,
)

router = APIRouter(prefix="/actions", tags=["actions"])

@router.post("/", response_model=ActionDTO)
async def create_new_action(action: ActionCreate, db: AsyncSession = Depends(get_db)):
    """Создание нового действия пользователя."""
    return await create_action(db, action)

@router.get("/{action_id}", response_model=ActionDTO)
async def read_action(action_id: int, db: AsyncSession = Depends(get_db)):
    """Получение действия пользователя по ID."""
    action_from_db = await get_action_by_id(db, action_id)
    if action_from_db is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return action_from_db

@router.get("/", response_model=list[ActionDTO])
async def read_all_actions(db: AsyncSession = Depends(get_db)):
    """Получение списка всех действий пользователей."""
    return await get_all_actions(db)