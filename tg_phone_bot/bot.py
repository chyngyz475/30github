import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import config
from handlers import admin, user
from keyboards import main_menu

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN, parse_mode="HTML")  # В 3.0.0 можно передавать parse_mode напрямую
dp = Dispatcher()

# Подключаем обработчики
dp.include_router(admin.router)
dp.include_router(user.router)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Привет! Выберите действие:", reply_markup=main_menu)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
