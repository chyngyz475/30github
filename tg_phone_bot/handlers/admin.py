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
