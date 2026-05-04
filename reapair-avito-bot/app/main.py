import uvicorn
from fastapi import FastAPI

from core.config import Settings
from core.logging import setup_logging

app = FastAPI(title="Avito AI Sales Agent")

# Импортируем API routers
from api.avito import router as avito_router
from api.telegram_bot import router as telegram_router

app.include_router(avito_router, prefix="/api/avito", tags=["avito"])
app.include_router(telegram_router, prefix="/api/telegram", tags=["telegram"])

# Инициализация логгера
setup_logging()

settings = Settings()

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}
    
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
from fastapi import APIRouter, Request, Response
from aiogram import Dispatcher
from services.telegram.bot import dp

router = APIRouter()

@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    json_data = await request.json()
    update = types.Update(**json_data)
    await dp.process_update(update)
    return Response(status_code=200)