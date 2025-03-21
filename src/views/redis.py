from fastapi import APIRouter, Depends
from src.dependencies.redis import get_redis

router = APIRouter()

@router.get("/ping")
async def ping_redis(redis=Depends(get_redis)):
    """Router to check if Redis is connected."""
    try:
        await redis.set("ping", "pong")  # Test write
        value = await redis.get("ping")  # Test read
        return {"status": "OK", "ping": value}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
