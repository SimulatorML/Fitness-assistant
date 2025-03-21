import json
from src.dependencies.redis import get_redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.message import Message
from llm.config_loader import CONFIG
from redis.asyncio import Redis


MAX_RECENT_MESSAGES = CONFIG.get("max_recent_messages", 20)


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
