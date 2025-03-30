import json
from src.dependencies.redis import get_redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.message import Message
from redis.asyncio import Redis
from src.database.models import SubSummary
from llm.config_loader import CONFIG
from llm.models import get_llm
from src.database.connection import session_maker
import logging

logger = logging.getLogger(__name__)

MAX_RECENT_MESSAGES = CONFIG.get("max_recent_messages", 20)
SUMMARY_SIZE = CONFIG.get("summary_chunk_size", 10)
MAX_SUMMARY_STACK = CONFIG.get("max_summary_stack", 10)  


async def save_message_to_redis(telegram_id: int, role: str, content: str, redis_client: Redis | None = None):
    """
    Save a message in Redis (short-term cache).
    """
    if not isinstance(content, str):
        raise ValueError("Cannot save non-string message content to Redis.")
    
    if redis_client is None:
        redis_client = await get_redis()

    key = f"user:{telegram_id}:history" 

    new_message = json.dumps({"role": role, "content": content})
    await redis_client.lpush(key, new_message)
    await redis_client.ltrim(key, 0, MAX_RECENT_MESSAGES - 1)


async def get_recent_messages(telegram_id: int, redis_client: Redis | None = None):
    """
    Retrieve recent messages from Redis using user_id.
    """
    if redis_client is None:
        redis_client = await get_redis()

    key = f"user:{telegram_id}:history" 

    messages = await redis_client.lrange(key, 0, MAX_RECENT_MESSAGES - 1)
    return [json.loads(msg) for msg in messages] if messages else []


async def save_message_to_db(telegram_id: int, role: str, content: str, db_session: AsyncSession):
    """
    Save a message permanently in PostgreSQL (long-term history).
    """
    if not isinstance(content, str):
        raise ValueError("Cannot save non-string message content to database.")
    
    new_message = Message(telegram_id=telegram_id, role=role, content=content) 
    db_session.add(new_message)
    await db_session.commit()


async def create_sub_summary(telegram_id: int, redis_client: Redis | None = None):
    redis_client = redis_client or await get_redis()
    key = f"user:{telegram_id}:history"

    messages = await redis_client.lrange(key, -SUMMARY_SIZE, -1)
    if not messages or len(messages) < SUMMARY_SIZE:
        return  # Not enough to summarize

    parsed = [json.loads(msg) for msg in messages]
    conversation_text = "\n".join(f"{m['role']}: {m['content']}" for m in parsed)

    llm = get_llm()
    prompt = f"""
    Condense the chat into a concise summary that captures the main points and themes.
    Use the user's language:\n\n{conversation_text}.
    """
    response = await llm.ainvoke(prompt)

    summary_key = f"user:{telegram_id}:sub_summaries"

    # Check if stack of sub-summaries is full
    current_stack = await redis_client.llen(summary_key)
    if current_stack >= MAX_SUMMARY_STACK:
        # Save to Postgres
        await save_sub_summaries_to_db(telegram_id, redis_client)
        await redis_client.delete(summary_key)  # Clear stack in Redis

    # Push new summary
    await redis_client.rpush(summary_key, response.content)

    # Trim recent history
    await redis_client.ltrim(key, SUMMARY_SIZE, -1)


async def is_stack_full(telegram_id: int, redis_client: Redis | None = None) -> bool:
    redis_client = redis_client or await get_redis()
    length = await redis_client.llen(f"user:{telegram_id}:history")
    return length == MAX_RECENT_MESSAGES


async def get_latest_sub_summary(telegram_id: int, redis_client: Redis | None = None) -> str | None:
    redis_client = redis_client or await get_redis()
    summary_key = f"user:{telegram_id}:sub_summaries"
    latest = await redis_client.lindex(summary_key, -1)
    return latest


async def save_sub_summaries_to_db(telegram_id: int, redis_client: Redis):
    summary_key = f"user:{telegram_id}:sub_summaries"
    summaries = await redis_client.lrange(summary_key, 0, -1)

    if not summaries:
        return

    async with session_maker() as session:
        for s in summaries:
            sub_summary = SubSummary(telegram_id=telegram_id, summary=s)
            session.add(sub_summary)
        await session.commit()