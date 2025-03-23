from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session
from database import get_db
from models import Phone, Request, User
from config import ADMIN_PASSWORD
from keyboards import get_admin_menu  # Будем реализовывать позже
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import GROUP_CHAT_ID

class AddPhone(StatesGroup):
    brand = State()
    model = State()
    price = State()
    condition = State()
    battery = State()
    description = State()
    photos = State()


class EditPhone(StatesGroup):
    waiting_for_field = State()
    waiting_for_value = State()

router = Router()

class AdminAuth(StatesGroup):
    password = State()

@router.message(Command("admin"))
async def cmd_admin(message: types.Message, state: FSMContext):
    await state.set_state(AdminAuth.password)
    await message.answer("🔑 Введите пароль администратора:")

@router.message(AdminAuth.password)
async def check_admin_password(message: types.Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        with next(get_db()) as session:
            user = session.query(User).filter_by(id=message.from_user.id).first()
            if not user:
                user = User(
                    id=message.from_user.id,
                    first_name=message.from_user.first_name,
                    username=message.from_user.username,
                    role="admin"
                )
                session.add(user)
            else:
                user.role = "admin"
            session.commit()
        await state.clear()
        await message.answer("✅ Вы вошли как администратор!", reply_markup=get_admin_menu())
    else:
        await message.answer("❌ Неверный пароль!")
        await state.clear()




@router.message(lambda message: message.text == "➕ Добавить телефон")
async def cmd_add_phone(message: types.Message, state: FSMContext):
    with next(get_db()) as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if user.role != "admin":
            return await message.answer("🚫 У вас нет прав!")
    await state.set_state(AddPhone.brand)
    await message.answer("Введите бренд телефона (например, Apple):")

@router.message(AddPhone.brand)
async def add_brand(message: types.Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await state.set_state(AddPhone.model)
    await message.answer("Введите модель телефона (например, iPhone 13):")

@router.message(AddPhone.model)
async def add_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await state.set_state(AddPhone.price)
    await message.answer("Введите цену в рублях:")

@router.message(AddPhone.price)
async def add_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        await state.update_data(price=price)
        await state.set_state(AddPhone.condition)
        await message.answer("Введите состояние (новый/б/у):")
    except ValueError:
        await message.answer("❌ Введите число!")

@router.message(AddPhone.condition)
async def add_condition(message: types.Message, state: FSMContext):
    await state.update_data(condition=message.text)
    await state.set_state(AddPhone.battery)
    await message.answer("Введите остаток батареи в % (или пропустите через /skip):")

@router.message(AddPhone.battery)
async def add_battery(message: types.Message, state: FSMContext):
    if message.text == "/skip":
        await state.update_data(battery=None)
    else:
        try:
            battery = int(message.text)
            await state.update_data(battery=battery)
        except ValueError:
            return await message.answer("❌ Введите число или /skip!")
    await state.set_state(AddPhone.description)
    await message.answer("Введите описание (или пропустите через /skip):")

@router.message(AddPhone.description)
async def add_description(message: types.Message, state: FSMContext):
    if message.text == "/skip":
        await state.update_data(description=None)
    else:
        await state.update_data(description=message.text)
    await state.set_state(AddPhone.photos)
    await message.answer("Загрузите 1-3 фото телефона (или завершите через /done):")

@router.message(AddPhone.photos, lambda message: message.photo)
async def add_photos(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photos = data.get("photos", [])
    if len(photos) >= 3:
        return await message.answer("❌ Лимит: 3 фото!")
    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)
    await message.answer(f"Фото добавлено ({len(photos)}/3). Загрузите еще или /done.")

@router.message(AddPhone.photos, Command("done"))
async def finish_adding(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if not data.get("photos"):
        return await message.answer("❌ Загрузите хотя бы одно фото!")
    with next(get_db()) as session:
        phone = Phone(
            admin_id=message.from_user.id,
            brand=data["brand"],
            model=data["model"],
            price=data["price"],
            condition=data["condition"],
            battery=data["battery"],
            description=data["description"],
            photos=data["photos"]
        )
        session.add(phone)
        session.commit()
        caption = f"📱 {phone.brand} {phone.model}\n💰 {phone.price} руб."
        await bot.send_photo(GROUP_CHAT_ID, phone.photos[0], caption=caption)
    await state.clear()
    await message.answer("✅ Телефон добавлен!")

@router.message(lambda message: message.text == "📋 Мои объявления")
async def my_ads(message: types.Message):
    with next(get_db()) as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if user.role != "admin":
            return await message.answer("🚫 У вас нет прав!")
        phones = session.query(Phone).filter_by(admin_id=message.from_user.id).all()
        if not phones:
            return await message.answer("📭 У вас нет объявлений.")
        for phone in phones:
            caption = (
                f"<b>📱 {phone.brand} {phone.model}</b>\n"
                f"💰 Цена: {phone.price} руб.\n"
                f"Статус: {phone.status}"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📝 Редактировать", callback_data=f"edit_{phone.id}")],
                [InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_{phone.id}")]
            ])
            await message.answer(caption, reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_phone(callback: CallbackQuery):
    phone_id = int(callback.data.split("_")[1])
    with next(get_db()) as session:
        phone = session.query(Phone).filter_by(id=phone_id, admin_id=callback.from_user.id).first()
        if phone:
            session.delete(phone)
            session.commit()
            await callback.message.answer("✅ Объявление удалено!")
            await callback.message.delete()
        else:
            await callback.answer("❌ Ошибка: нет прав или объявление не найдено.", show_alert=True)

@router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_phone(callback: CallbackQuery, state: FSMContext):
    phone_id = int(callback.data.split("_")[1])
    await state.update_data(phone_id=phone_id)
    await callback.message.answer("Введите новое значение для цены:")
    await state.set_state("edit_price")  # Упрощенный пример, можно расширить



@router.callback_query(lambda c: c.data.startswith("edit_"))
async def start_edit_phone(callback: CallbackQuery, state: FSMContext):
    phone_id = int(callback.data.split("_")[1])
    with next(get_db()) as session:
        phone = session.query(Phone).filter_by(id=phone_id, admin_id=callback.from_user.id).first()
        if not phone:
            await callback.answer("❌ Нет прав или объявление не найдено.", show_alert=True)
            return
    await state.update_data(phone_id=phone_id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Цена", callback_data="field_price")],
        [InlineKeyboardButton(text="🛠 Состояние", callback_data="field_condition")],
        [InlineKeyboardButton(text="🔋 Батарея", callback_data="field_battery")],
        [InlineKeyboardButton(text="📌 Описание", callback_data="field_description")],
        [InlineKeyboardButton(text="📸 Фото", callback_data="field_photos")]
    ])
    await callback.message.answer("Выберите, что изменить:", reply_markup=keyboard)
    await state.set_state(EditPhone.waiting_for_field)
    await callback.answer()

@router.callback_query(EditPhone.waiting_for_field)
async def select_field(callback: CallbackQuery, state: FSMContext):
    field = callback.data.split("_")[1]
    await state.update_data(field=field)
    if field == "photos":
        await callback.message.answer("Загрузите новые фото (до 3-х):")
    else:
        await callback.message.answer(f"Введите новое значение для {field}:")
    await state.set_state(EditPhone.waiting_for_value)
    await callback.answer()

@router.message(EditPhone.waiting_for_value, lambda message: not message.photo)
async def save_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_id, field = data["phone_id"], data["field"]

    with next(get_db()) as session:
        phone = session.query(Phone).filter_by(id=phone_id).first()
        if field in ["price", "battery"]:
            try:
                value = int(message.text) if message.text != "/skip" else None
            except ValueError:
                return await message.answer("❌ Введите число или /skip!")
        else:
            value = message.text if message.text != "/skip" else None
        setattr(phone, field, value)
        session.commit()
    await message.answer(f"✅ Поле {field} обновлено!")
    await state.clear()

@router.message(EditPhone.waiting_for_value, lambda message: message.photo)
async def save_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_id = data["phone_id"]
    photos = data.get("photos", [])

    if len(photos) >= 3:
        return await message.answer("❌ Лимит: 3 фото!")
    photos.append(message.photo[-1].file_id)

    await state.update_data(photos=photos)
    if len(photos) < 3:
        await message.answer(f"Фото добавлено ({len(photos)}/3). Загрузите еще или /done.")
    else:
        with next(get_db()) as session:
            phone = session.query(Phone).filter_by(id=phone_id).first()
            phone.photos = photos
            session.commit()
        await message.answer("✅ Фото обновлены!")
        await state.clear()

@router.message(EditPhone.waiting_for_value, Command("done"))
async def finish_edit_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_id, photos = data["phone_id"], data.get("photos", [])
    if not photos:
        return await message.answer("❌ Загрузите хотя бы одно фото!")
    with next(get_db()) as session:
        phone = session.query(Phone).filter_by(id=phone_id).first()
        phone.photos = photos
        session.commit()
    await message.answer("✅ Фото обновлены!")
    await state.clear()


@router.message(lambda message: message.text == "📩 Заявки")
async def list_requests(message: types.Message):
    with next(get_db()) as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if user.role != "admin":
            return await message.answer("🚫 У вас нет прав!")
        requests = session.query(Request).join(Phone).filter(Phone.admin_id == message.from_user.id).all()
        if not requests:
            return await message.answer("📭 Заявок пока нет.")
        for req in requests:
            phone = session.query(Phone).filter_by(id=req.phone_id).first()
            caption = (
                f"📩 Заявка ID: {req.id}\n"
                f"Телефон: {phone.brand} {phone.model}\n"
                f"Пользователь: @{req.user_id}\n"
                f"Статус: {req.status}"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⏳ В обработке", callback_data=f"req_process_{req.id}")],
                [InlineKeyboardButton(text="✅ Завершена", callback_data=f"req_complete_{req.id}")]
            ])
            await message.answer(caption, reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("req_"))
async def update_request_status(callback: CallbackQuery):
    action, req_id = callback.data.split("_")[1], int(callback.data.split("_")[2])
    with next(get_db()) as session:
        request = session.query(Request).filter_by(id=req_id).first()
        if action == "process":
            request.status = "processing"
            await callback.message.answer("✅ Заявка переведена в обработку.")
        elif action == "complete":
            request.status = "completed"
            phone = session.query(Phone).filter_by(id=request.phone_id).first()
            phone.status = "sold"
            await callback.message.answer("✅ Заявка завершена, телефон помечен как проданный.")
        session.commit()
    await callback.message.edit_reply_markup(None)  # Убираем кнопки
    await callback.answer()