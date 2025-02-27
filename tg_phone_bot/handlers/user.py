from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.orm import Session
from database import get_db
from models import Phone

router = Router()

# Команда /list для просмотра всех объявлений
@router.message(Command("list"))
async def list_phones(message: types.Message, session: Session = get_db()):
    phones = session.query(Phone).filter(Phone.status == "Активно").all()

    if not phones:
        await message.answer("📭 Объявлений пока нет!")
        return

    for phone in phones:
        caption = (
            f"<b>📱 {phone.brand} {phone.model}</b>\n"
            f"💰 Цена: {phone.price} руб.\n"
            f"🔋 Батарея: {phone.battery}%\n"
            f"🛠 Состояние: {phone.condition}\n"
            f"📌 Описание: {phone.description}"
        )
        
        photos = phone.photos
        media = [types.InputMediaPhoto(photo, caption=caption if i == 0 else "") for i, photo in enumerate(photos)]
        
        if media:
            await message.answer_media_group(media)
        else:
            await message.answer(caption)

    await message.answer("📭 Объявлений пока нет!")