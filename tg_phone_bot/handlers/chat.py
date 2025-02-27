from aiogram import Router, types
from aiogram.types import CallbackQuery
from database import get_db
from sqlalchemy.orm import Session
from tg_phone_bot import bot

router = Router()
chat_sessions = {}  # Временное хранилище чатов (ключ: покупатель, значение: продавец)

@router.callback_query(lambda c: c.data.startswith("chat_"))
async def start_chat(callback: CallbackQuery, session: Session = get_db()):
    seller_id = int(callback.data.split("_")[1])
    buyer_id = callback.from_user.id

    chat_sessions[buyer_id] = seller_id
    chat_sessions[seller_id] = buyer_id  # Двусторонняя связь

    await callback.message.answer("✅ Вы начали чат с продавцом. Напишите сообщение:")
    await bot.send_message(seller_id, f"📩 Покупатель @{callback.from_user.username} хочет связаться с вами!")

@router.message()
async def forward_message(message: types.Message):
    user_id = message.from_user.id

    if user_id in chat_sessions:
        recipient_id = chat_sessions[user_id]
        await bot.send_message(recipient_id, f"💬 Сообщение от @{message.from_user.username}:\n{message.text}")
