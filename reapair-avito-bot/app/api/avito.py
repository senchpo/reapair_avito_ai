from fastapi import APIRouter, Request, status, Depends, HTTPException
import logging

from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

logger = logging.getLogger("avito-webhook")

@router.post("/webhook")
async def avito_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    payload = await request.json()
    logger.info(f"Incoming Avito webhook payload: {payload}")

    # TODO: валидация webhook, обработка события,
    # кладём в очередь для асинхронной обработки

    return {"status": "accepted"}