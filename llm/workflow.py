from datetime import datetime
from fastapi import HTTPException
#from src.dependencies.redis import get_redis
from langchain_core.prompts import ChatPromptTemplate
from llm.models import get_llm
from src.utils import get_user
from src.dependencies import DBSession
from src.schemas.user import UserDTO
from llm.chat_memory import (
    get_recent_messages,
    save_message_to_redis,
    save_message_to_db,
    is_stack_full,
    create_sub_summary,
    get_latest_sub_summary,
)
import logging

logger = logging.getLogger(__name__)

llm = get_llm()

SYSTEM_PROMPT = """
You are an AI fitness assistant. Your job is to provide users with expert-level fitness, nutrition, and workout recommendations.
You should personalize responses based on the user's fitness level, goals, and other relevant details.
Be precise, encouraging, and professional. Keep answers concise but informative.

Always respond in the same language as the user's question, unless the user explicitly requests a different language.
If the question contains multiple languages, prioritize the primary language of the query.
"""


async def get_user_info(telegram_id: int, session: DBSession) -> UserDTO:
    """
    Retrieves user details from the database based on telegram_id..
    """
    user = await get_user(telegram_id, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")
    
    return UserDTO.model_validate(user)


async def process_fitness_query(user_query: str, telegram_id: int, session: DBSession) -> str:
    """
    Processes a user query with user info and returns an AI-generated response.

    Args:
        user_query (str): The question asked by the user.
        telegram_id (int): The Telegram user's ID.
        session (DBSession): The database session.

    Returns:
        str: The AI-generated response.
    """

    user_info = await get_user_info(telegram_id, session)
    user_info_text = user_info.model_dump_json(indent=2)

    resent_chat_history = await get_recent_messages(telegram_id)

    if await is_stack_full(telegram_id):
        await create_sub_summary(telegram_id)

    latest_summary = await get_latest_sub_summary(telegram_id)
    summary_text = latest_summary or ""

    logger.info(f"📌 Latest summary: {summary_text}")

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("system", "Previous conversation summary:\n{summary_text}"),
            ("human", "User Info:\n{user_info_text}\n\n"),
            ("human", "Chat history:\n{chat_history}\n\n"),
            ("human", "User Question:\n{query}"),
        ]
    )

    chain = chat_prompt | llm

    response = await chain.ainvoke(
        {
            "summary_text": summary_text,
            "query": user_query,
            "user_info_text": user_info_text,
            "chat_history": resent_chat_history,
        }
    )

    content = getattr(response, "content", None)
    if not content:
        raise HTTPException(status_code=500, detail="LLM returned an empty response.")

    await save_message_to_redis(telegram_id, "user", user_query)
    await save_message_to_redis(telegram_id, "assistant", content)
    await save_message_to_db(telegram_id, "user", user_query, session)
    await save_message_to_db(telegram_id, "assistant", content, session)

    return content
