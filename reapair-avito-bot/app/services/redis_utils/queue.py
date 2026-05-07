import asyncio
import aioredis
import json
from typing import Any, Dict

class RedisQueue:
    def __init__(self, redis_url: str, queue_name: str):
        self.redis_url = redis_url
        self.queue_name = queue_name
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)

    async def enqueue(self, message: Dict[str, Any]):
        """
        Помещаем сообщение в очередь в виде JSON строки
        """
        if not self.redis:
            await self.connect()
        msg_str = json.dumps(message)
        await self.redis.lpush(self.queue_name, msg_str)

    async def dequeue(self) -> Dict[str, Any]:
        if not self.redis:
            await self.connect()
        msg_str = await self.redis.rpop(self.queue_name)
        if msg_str:
            return json.loads(msg_str)
        return {}

    async def listen(self, handler):
        """
        Бесконечно слушаем очередь и вызываем handler для каждого сообщения.
        Handler — короутина, принимает распарсенное сообщение
        """
        if not self.redis:
            await self.connect()

        while True:
            msg = await self.dequeue()
            if msg:
                await handler(msg)
            else:
                await asyncio.sleep(1)  # Очередь пуста, пауза