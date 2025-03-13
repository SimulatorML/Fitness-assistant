from langchain_core.prompts import ChatPromptTemplate
from llm.models import get_llm
from src.views.users import get_user
from src.dependencies import DBSession
from fastapi import HTTPException
from collections import defaultdict

llm = get_llm()

SYSTEM_PROMPT = """
You are an AI fitness assistant. Your job is to provide users with expert-level fitness, nutrition, and workout recommendations.
You should personalize responses based on the user's fitness level, goals, and other relevant details.
Be precise, encouraging, and professional. Keep answers concise but informative.
"""

# In-memory storage for chat history: {user_id: [(user_input, ai_response)]} 
# We should use a DB for production
chat_history_store = defaultdict(list)  


async def get_user_info_dict(user_id: int, session: DBSession) -> dict:
    """
    Retrieves user details from the database based on user_id.
    Uses mock user data if database is unavailable.
    """
    try:
        user_info = await get_user(user_id, session)
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found")
        user_info_dict = user_info.model_dump()

    # use mock data (remove in future)
    except Exception:
        user_info_dict = {
            "id": user_id,
            "name": "Test User",
            "age": 30,
            "activity_level": "moderate",
            "goal": "muscle_gain",
        }

    return user_info_dict


async def process_fitness_query(
    user_query: str, user_id: int, session: DBSession
) -> str:
    """
    Processes a user query with user info and returns an AI-generated response.

    Args:
        user_query (str): The question asked by the user.
        user_id (int): The user's ID.
        session (DBSession): The database session.

    Returns:
        str: The AI-generated response.
    """

    user_info_dict = await get_user_info_dict(user_id, session)

    chat_history = chat_history_store[user_id]

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

    chat_history_store[user_id].append((user_query, content))

    return content
