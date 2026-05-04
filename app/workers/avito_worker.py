import asyncio
import json
import logging

from services.redis_utils.queue import dequeue_message

logger = logging.getLogger("worker")

async def process_message(message: dict):
    # Здесь логика обработки сообщений
    logger.info(f"Processing message: {message}")
    # ... бизнес-логика, вызовы AI и т.д.

async def worker():
    while True:
        raw_message = await dequeue_message()
        message = json.loads(raw_message)
        await process_message(message)
        await asyncio.sleep(0.1)  # Небольшая пауза, чтобы избежать перегрузки

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    asyncio.run(worker())