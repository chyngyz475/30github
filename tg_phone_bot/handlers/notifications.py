from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.orm import Session
from database import get_db
from models import Subscriber, Phone
from aiogram.filters import Command
from tg_phone_bot import bot


router = Router()

# Команда подписки
@router.message(Command("subscribe"))
async def subscribe(message: types.Message, session: Session = get_db()):
    user_id = message.from_user.id

    if session.query(Subscriber).filter_by(user_id=user_id).first():
        await message.answer("✅ Вы уже подписаны на уведомления!")
    else:
        session.add(Subscriber(user_id=user_id))
        session.commit()
        await message.answer("✅ Вы подписались на уведомления о новых объявлениях!")

# Команда отписки
@router.message(Command("unsubscribe"))
async def unsubscribe(message: types.Message, session: Session = get_db()):
    user_id = message.from_user.id

    sub = session.query(Subscriber).filter_by(user_id=user_id).first()
    if sub:
        session.delete(sub)
        session.commit()
        await message.answer("❌ Вы отписались от уведомлений.")
    else:
        await message.answer("🚫 Вы не были подписаны.")

# Уведомление о новом объявлении
async def notify_subscribers(phone: Phone, session: Session):
    subscribers = session.query(Subscriber).all()
    
    caption = (
        f"<b>📱 Новое объявление: {phone.brand} {phone.model}</b>\n"
        f"💰 Цена: {phone.price} руб.\n"
        f"🔋 Батарея: {phone.battery}%\n"
        f"📌 Описание: {phone.description}\n"
        f"👤 Продавец: @{phone.username}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📩 Написать продавцу", callback_data=f"chat_{phone.user_id}")]
        ]
    )

    for sub in subscribers:
        try:
            await bot.send_message(sub.user_id, caption, reply_markup=keyboard)
        except:
            pass  # Ошибки игнорируем, если пользователь заблокировал бота
