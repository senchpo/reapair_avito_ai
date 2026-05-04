from aiogram import types
from services.telegram.bot import dp

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот уведомлений сервиса Avito.")

async def send_notification(chat_id: int, text: str):
    from services.telegram.bot import bot
    await bot.send_message(chat_id, text)