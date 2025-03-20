from langchain_core.prompts import ChatPromptTemplate
from llm.models import get_llm
from src.utils import get_user
from src.dependencies import DBSession
from fastapi import HTTPException
from collections import defaultdict
from datetime import datetime
from src.schemas.user import UserDTO


llm = get_llm()

SYSTEM_PROMPT = """
You are an AI fitness assistant. Your job is to provide users with expert-level fitness, nutrition, and workout recommendations.
You should personalize responses based on the user's fitness level, goals, and other relevant details.
Be precise, encouraging, and professional. Keep answers concise but informative.

Always respond in the same language as the user's question, unless the user explicitly requests a different language.
If the question contains multiple languages, prioritize the primary language of the query.
"""

# In-memory storage for chat history: {telegram_id: [(user_input, ai_response)]} 
# We should use a DB for production
chat_history_store = defaultdict(list)  


async def get_user_info_dict(telegram_id: int, session: DBSession) -> dict:
    """
    Retrieves user details from the database based on telegram_id.
    Converts user data automatically to a dictionary.
    """
    user_info = await get_user(telegram_id, session)

    if not user_info:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")

    # Convert the SQLAlchemy model to a dictionary
    user_info_dict = UserDTO.model_validate(user_info).dict() 

    user_info_dict["age"] = datetime.now().year - user_info.birth_date.year  

    return user_info_dict


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

    user_info_dict = await get_user_info_dict(telegram_id, session)

    chat_history = chat_history_store[telegram_id]

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "User Info:\n{user_info_text}\n\n"),
            ("human", "Chat history:\n{chat_history}\n\n"),
            ("human", "User Question:\n{query}"),
        ]
    )

    chain = chat_prompt | llm

    response = chain.invoke(
        {
            "query": user_query,
            "user_info_text": user_info_dict,
            "chat_history": chat_history,
        }
    )

    content = response.content

    # Save conversation history
    chat_history_store[telegram_id].append((user_query, content))

    return content
