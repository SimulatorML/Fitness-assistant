from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from llm.workflow import process_fitness_query
from src.database.connection import get_db  # ДОБАВИТЬ
from sqlalchemy.ext.asyncio import AsyncSession  # ДОБАВИТЬ
from typing import Any

router = APIRouter(prefix="/llm", tags=["llm"])

class LLMRequest(BaseModel):
    query: str
    user_id: int
    metadata: dict[str, Any] = {}

class LLMResponse(BaseModel):
    status: str
    response: str
    additional_info: dict[str, Any] = {}


@router.post("/message", response_model=LLMResponse)  # Изменили путь
async def llm_request(data: LLMRequest, session: AsyncSession = Depends(get_db)) -> LLMResponse:  #  Depends
    try:
        response = await process_fitness_query(data.query, data.user_id, session)
        return LLMResponse(status="ok", response=response)  # Используем модель
    except Exception as e:
        # Логируем ошибку (обязательно!)
        print(f"Error in llm_request: {e}")  # Или logger
        return LLMResponse(status="error", response="Sorry, something went wrong.")