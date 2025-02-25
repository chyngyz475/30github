import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import init_db, get_db
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Клавиатура
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("Добавить телефон"), KeyboardButton("Мои телефоны"))

@dp.message(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет! Этот бот поможет тебе продать телефон 📱", reply_markup=main_kb)

@dp.message(lambda message: message.text == "Добавить телефон")
async def add_phone(message: types.Message):
    await message.answer("Введите бренд телефона (например, Samsung, iPhone):")
    dp.register_message_handler(get_brand, state="brand")

async def get_brand(message: types.Message, state):
    brand = message.text
    await state.update_data(brand=brand)
    await message.answer("Теперь введите модель:")
    dp.register_message_handler(get_model, state="model")

async def get_model(message: types.Message, state):
    model = message.text
    user_data = await state.get_data()
    brand = user_data["brand"]
    
    async with await get_db() as db:
        await db.execute("INSERT INTO phones (user_id, brand, model) VALUES ($1, $2, $3)", message.from_user.id, brand, model)
    
    await message.answer(f"Телефон {brand} {model} добавлен!", reply_markup=main_kb)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
