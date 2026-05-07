import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.config import settings
from core.logging import setup_logging
from db.session import init_db, get_session, engine
from services.ai.openai_client import AIClient
from services.ai.summary import SummaryEngine
from services.bitrix.integration import BitrixClient
from redis.queue import RedisQueue
from services.orchestrator import MessageOrchestrator
from api.webhooks import router as webhooks_router
from services.telegram.control_panel import router as telegram_router
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

# Глобальные сервисы
services = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация и закрытие ресурсов"""
    setup_logging(settings.LOG_LEVEL)
    logger.info("Запуск приложения...")

    # 1. Инициализация БД
    await init_db()
    logger.info("БД инициализирована")

    # 2. AI клиент
    openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    services["ai_client"] = AIClient(
        client=openai_client,
        model=settings.OPENAI_MODEL,
    )
    services["summary_engine"] = SummaryEngine(
        openai_client=openai_client,
        model=settings.OPENAI_MODEL,
    )
    logger.info("AI сервисы готовы")

    # 3. Bitrix клиент
    services["bitrix"] = BitrixClient(
        api_token=settings.BITRIX_API_TOKEN,
        base_url=settings.BITRIX_BASE_URL,
    )
    logger.info("Bitrix клиент готов")

    # 4. Redis Queue
    redis_queue = RedisQueue(
        redis_url=settings.REDIS_URL,
        queue_name="lead_messages",
    )
    await redis_queue.connect()
    services["redis_queue"] = redis_queue
    logger.info("Redis подключен")

    # 5. Запуск воркера очереди в фоне
    worker_task = asyncio.create_task(start_queue_worker(redis_queue))
    logger.info("Воркер очереди запущен")

    logger.info("Приложение готово к работе")
    yield

    # Завершение
    logger.info("Остановка приложения...")
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass
    await engine.dispose()
    logger.info("Ресурсы освобождены")


async def start_queue_worker(redis_queue: RedisQueue):
    """Фоновый воркер для обработки задач из очереди"""
    async def handler(msg):
        msg_type = msg.get("type")
        logger.info(f"Обработка задачи из очереди: {msg_type}")

        if msg_type == "ai_response":
            # Например: отправить ответ обратно в канал (Avito/WhatsApp/Telegram)
            logger.info(f"AI response для {msg.get('lead_id')}: {msg.get('response')[:100]}")
        elif msg_type == "human_notification":
            # Уведомление менеджера в Telegram
            logger.info(f"Уведомление менеджеру по лиду {msg.get('lead_id')}")
        elif msg_type == "error":
            logger.error(f"Ошибка по лиду {msg.get('lead_id')}: {msg.get('error')}")

    try:
        await redis_queue.listen(handler)
    except asyncio.CancelledError:
        logger.info("Воркер очереди остановлен")
        raise


# Создание приложения
app = FastAPI(
    title="AI Lead Bot",
    version="1.0.0",
    lifespan=lifespan,
)

# Подключение роутеров
app.include_router(webhooks_router, prefix="/webhooks", tags=["webhooks"])
app.include_router(telegram_router, prefix="/telegram", tags=["telegram"])


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "service": "AI Lead Bot",
        "version": "1.0.0",
        "status": "running",
    }


# Точка входа в Orchestrator (для использования в обработчиках)
async def get_orchestrator() -> MessageOrchestrator:
    async with get_session() as session:
        return MessageOrchestrator(
            session=session,
            ai_client=services["ai_client"],
            summary_engine=services["summary_engine"],
            bitrix=services["bitrix"],
            redis_queue=services["redis_queue"],
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )