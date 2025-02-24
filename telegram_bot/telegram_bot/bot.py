import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from config import TOKEN
from auth.register import register_new_account
from auth.account_manager import get_account

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Отправь ссылку на сайт, и я попробую спарсить данные. Также ты можешь зарегистрировать аккаунт командой /register.")

@dp.message(Command("register"))
async def register(message: Message):
    result = await register_new_account()
    if "error" in result:
        await message.answer(f"❌ Ошибка регистрации: {result['error']}")
    else:
        await message.answer(f"✅ Новый аккаунт создан:\nEmail: {result['email']}\nПароль: {result['password']}")

@dp.message(Command("account"))
async def get_account_info(message: Message):
    account = get_account()
    if account:
        await message.answer(f"🔐 Текущий аккаунт:\nEmail: {account['email']}\nПароль: {account['password']}")
    else:
        await message.answer("❌ В базе нет зарегистрированных аккаунтов.")
        


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
