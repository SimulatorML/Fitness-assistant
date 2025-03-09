import logging
from collections import defaultdict
from datetime import datetime
from typing import List, Tuple, Dict, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.prompts import ChatPromptTemplate
from llm.models import llm
from src.services.user_service import get_user_by_telegram_id
from src.services.llm_service import send_request_to_llm  # ⚡ Используем сервис
from src.database.models import Action
from src.schemas.action import ActionType, ActionCreate

# Настроим логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Системный промпт
SYSTEM_PROMPT = """
You are an AI fitness assistant. Your job is to provide users with expert-level fitness, nutrition, and workout recommendations.
You should personalize responses based on the user's fitness level, goals, and other relevant details.
Be precise, encouraging, and professional. Keep answers concise but informative.
"""

# In-memory хранилище истории чата (в production использовать БД)
chat_history_store: Dict[int, List[Tuple[str, str]]] = defaultdict(list)


async def get_user_info_dict(user_id: int, session: AsyncSession) -> Optional[Dict]:
    """Получает информацию о пользователе из базы данных."""
    try:
        user_info = await get_user_by_id(user_id, session)
        return user_info.model_dump() if user_info else None
    except Exception as e:
        logging.error(f"❌ Ошибка получения данных пользователя {user_id}: {e}", exc_info=True)
        return None


async def format_user_info(user_info: Dict) -> str:
    """Форматирует информацию о пользователе для промпта."""
    activities = user_info.get("preferred_activities", [])
    activities_str = ", ".join(activities) if activities else "Не указано"
    birth_date = user_info.get("birth_date", "Не указано")
    if isinstance(birth_date, datetime):
        birth_date = birth_date.strftime("%d.%m.%Y")

    return (
        f"Имя: {user_info.get('name', 'Не указано')}\n"
        f"Дата рождения: {birth_date}\n"
        f"Пол: {user_info.get('gender', 'Не указано')}\n"
        f"Рост: {user_info.get('height', 'Не указано')} см\n"
        f"Вес: {user_info.get('weight', 'Не указано')} кг\n"
        f"Уровень активности: {user_info.get('activity_level', 'Не указано')}\n"
        f"Цель: {user_info.get('goal', 'Не указано')}\n"
        f"Ограничения: {user_info.get('health_restrictions', 'Не указано')}\n"
        f"Активности: {activities_str}\n"
    )


async def format_chat_history(chat_history: List[Tuple[str, str]]) -> str:
    """Форматирует историю чата для LLM."""
    return "\n".join(f"Пользователь: {user_msg}\nАссистент: {ai_msg}" for user_msg, ai_msg in chat_history)


async def process_fitness_query(user_query: str, user_id: int, session: AsyncSession) -> str:
    """
    Формирует запрос к LLM, добавляя данные пользователя и историю чата.
    Отправляет запрос в `send_request_to_llm()` и возвращает ответ.
    """
    # Получаем информацию о пользователе
    user_info_dict = await get_user_info_dict(user_id, session)
    if not user_info_dict:
        raise HTTPException(status_code=404, detail="User not found")

    formatted_user_info = await format_user_info(user_info_dict)
    formatted_history = await format_chat_history(chat_history_store[user_id])

    # Генерируем промпт
    prompt_template = ChatPromptTemplate.from_template(
        f"{SYSTEM_PROMPT}\n\nUser Info:\n{{user_info}}\n\nChat History:\n{{chat_history}}\n\nUser Query: {{user_query}}\n\n"
    )
    prompt = prompt_template.format(
        user_info=formatted_user_info,
        chat_history=formatted_history,
        user_query=user_query,
    )

    logging.info(f"📝 Отправка запроса к LLM: {user_query}")
    try:
        # ⚡ Отправляем запрос через `llm_service`
        ai_response = await send_request_to_llm(prompt)
        logging.info("✅ LLM успешно ответил.")

        # Обновляем историю чата
        chat_history_store[user_id].append((user_query, ai_response.get("response", "Нет ответа")))

        return ai_response.get("response", "Нет ответа")
    except Exception as e:
        logging.error(f"❌ Ошибка при обработке запроса LLM: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ошибка обработки запроса")
