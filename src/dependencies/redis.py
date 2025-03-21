import redis.asyncio as aioredis
import os
import dotenv


dotenv.load_dotenv() 

REDIS_HOST = os.environ.get("REDIS_HOST", "redis") 
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))

_redis_client: aioredis.Redis | None = None


async def startup():
    """Initialize Redis connection when FastAPI starts."""
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


async def shutdown():
    """Close Redis connection when FastAPI stops."""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


def get_redis():
    """Return Redis connection."""
    if _redis_client is None:
        raise RuntimeError("Redis is not initialized. Call startup() first.")
    return _redis_client
