from services.redis_utils.redis_client import get_redis
from services.redis_utils.locks import RedisLock
import asyncio

LOCK_KEY_PREFIX = "conversation_owner_lock:"

class OwnershipService:
    def __init__(self):
        self.redis = None

    async def init(self):
        if not self.redis:
            self.redis = await get_redis()

    async def acquire_ownership(self, conversation_id: int, owner_id: str, timeout=30) -> bool:
        await self.init()
        lock_key = f"{LOCK_KEY_PREFIX}{conversation_id}"
        lock = RedisLock(self.redis, lock_key, ttl=timeout)
        success = await lock.acquire()
        if success:
            # Тут можно добавить привязку owner_id к записи conversation в БД (dao)
            return True
        return False

    async def release_ownership(self, conversation_id: int) -> bool:
        if not self.redis:
            await self.init()
        lock_key = f"{LOCK_KEY_PREFIX}{conversation_id}"
        lock = RedisLock(self.redis, lock_key)
        return await lock.release()