import asyncio
from services.redis_utils.redis_client import get_redis

QUEUE_NAME = "avito_incoming_messages"

async def enqueue_message(message: dict):
    redis = await get_redis()
    await redis.lpush(QUEUE_NAME, str(message))  # Сохраняем сериализованный dict как строку

async def dequeue_message():
    redis = await get_redis()
    # BRPOP - блокирующее ожидание
    _, item = await redis.brpop(QUEUE_NAME)
    return item  # Нужно десериализовать из строки в dict (например json.loads)