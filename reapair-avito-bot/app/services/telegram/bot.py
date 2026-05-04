from aiogram import Bot, Dispatcher, types

from core.config import settings

bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher(bot)