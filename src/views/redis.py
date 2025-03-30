from fastapi import APIRouter, Depends
from src.dependencies.redis import get_redis
import json

router = APIRouter(prefix="/redis", tags=["redis"])


@router.get("/ping")
async def ping_redis(redis=Depends(get_redis)):
    """Router to check if Redis is connected."""
    try:
        await redis.set("ping", "pong")  # Test write
        value = await redis.get("ping")  # Test read
        return {"status": "OK", "ping": value}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


@router.get("/history")
async def get_redis_history(telegram_id: int, redis=Depends(get_redis)):
    """Return decoded Redis history and sub_summaries for a user."""
    history_raw = await redis.lrange(f"user:{telegram_id}:history", 0, -1)
    sub_summaries = await redis.lrange(f"user:{telegram_id}:sub_summaries", 0, -1)

    history = [json.loads(m) for m in history_raw]

    # sub-summaries are reversed to show in chronological order
    return {"history": history, "sub_summaries": sub_summaries[::-1]} 