import aioredis
from core.config import Settings

settings = Settings()

redis = None

async def get_redis():
    global redis
    if not redis:
        redis = await aioredis.from_url(settings.redis_dsn, encoding="utf-8", decode_responses=True)
    return redis