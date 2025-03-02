from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import config
from keyboards import main_menu

router = Router()

class AdminAuth(StatesGroup):
    password = State()

@router.message(Command("admin"))
@router.message(lambda message: message.text == "🔑 Админ")
async def request_admin_password(message: types.Message, state: FSMContext):
    await state.set_state(AdminAuth.password)
    await message.answer("🔑 Введите пароль администратора:")

@router.message(AdminAuth.password)
async def check_admin_password(message: types.Message, state: FSMContext):
    if message.text == config.ADMIN_PASSWORD:
        config.ADMIN_ID = message.from_user.id  # Запоминаем ID администратора
        await state.clear()
        await message.answer("✅ Вы вошли в режим администратора!", reply_markup=main_menu)
    else:
        await message.answer("❌ Неверный пароль!")

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

@router.message(Command("my_ads"))
async def my_ads(message: types.Message):
    session: Session = get_db()
    phones = session.query(Phone).filter_by(admin_id=message.from_user.id).all()
    session.close()

    if not phones:
        return await message.answer("📌 У вас пока нет объявлений.")

    for phone in phones:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✏ Редактировать", callback_data=f"edit_{phone.id}")],
            [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{phone.id}")]
        ])
        await message.answer(
            f"📱 *{phone.brand} {phone.model}*\n💰 Цена: {phone.price} руб.\n🔋 Батарея: {phone.battery}%\n\n🆔 ID: `{phone.id}`",
            parse_mode="Markdown",
            reply_markup=keyboard
        )

    session.close()