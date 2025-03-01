from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.orm import Session
from database import get_db
from models import Phone
import config

router = Router()

@router.message(Command("delete"))
async def delete_phone(message: types.Message):
    # Проверяем, передан ли ID
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("⚠ Укажите ID телефона, который хотите удалить.\nПример: `/delete 123`", parse_mode="Markdown")

    phone_id = args[1]

    session: Session = get_db()
    phone = session.query(Phone).filter_by(id=phone_id, admin_id=message.from_user.id).first()

    if not phone:
        session.close()
        return await message.answer("🚫 Телефон не найден или у вас нет прав на его удаление.")

    session.delete(phone)
    session.commit()
    session.close()

    await message.answer(f"✅ Телефон с ID {phone_id} успешно удален!")
