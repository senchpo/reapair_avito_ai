import asyncio
from aioredis.client import Redis
from typing import Optional

class RedisLock:
    def __init__(self, redis: Redis, key: str, ttl: int = 30):
        self.redis = redis
        self.key = key
        self.ttl = ttl
        self.lock_value = None

    async def acquire(self) -> bool:
        # Уникальное значение для блокировки (например, process id + таймстамп)
        import uuid
        self.lock_value = str(uuid.uuid4())
        acquired = await self.redis.set(self.key, self.lock_value, nx=True, ex=self.ttl)
        return acquired

    async def release(self) -> bool:
        # Отпускаем только если значение совпадает (актуально для avoiding deadlocks)
        script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        res = await self.redis.eval(script, keys=[self.key], args=[self.lock_value])
        return res == 1