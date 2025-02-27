from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlalchemy.orm import Session
from database import get_db
from models import Phone
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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
    


class SearchState(StatesGroup):
    query = State()

# Команда /search
@router.message(Command("search"))
async def start_search(message: Message, state: FSMContext):
    await message.answer("🔎 Введите марку, модель или ценовой диапазон (например, 'iPhone', 'Samsung' или 'до 40000'):")
    await state.set_state(SearchState.query)

# Обрабатываем ввод пользователя
@router.message(SearchState.query)
async def process_search(message: Message, state: FSMContext, session: Session = get_db()):
    query = message.text.lower().strip()

    # Поиск по марке и модели
    phones = session.query(Phone).filter(
        (Phone.brand.ilike(f"%{query}%")) |
        (Phone.model.ilike(f"%{query}%")) |
        (Phone.price <= int(query.replace("до ", ""))) if "до" in query else False
    ).all()

    await state.clear()

    if not phones:
        await message.answer("❌ Ничего не найдено. Попробуйте другой запрос.")
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


# 1. Команда для просмотра своих объявлений
@router.message(Command("my_ads"))
async def my_ads(message: types.Message, session: Session = get_db()):
    user_id = message.from_user.id
    phones = session.query(Phone).filter(Phone.user_id == user_id).all()

    if not phones:
        await message.answer("📭 У вас пока нет объявлений.")
        return

    for phone in phones:
        caption = (
            f"<b>📱 {phone.brand} {phone.model}</b>\n"
            f"💰 Цена: {phone.price} руб.\n"
            f"🔋 Батарея: {phone.battery}%\n"
            f"🛠 Состояние: {phone.condition}\n"
            f"📌 Описание: {phone.description}"
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📝 Редактировать", callback_data=f"edit_{phone.id}")],
                [InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_{phone.id}")]
            ]
        )

        await message.answer(caption, reply_markup=keyboard)

# 2. Обработчик удаления объявления
@router.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_ad(callback: CallbackQuery, session: Session = get_db()):
    ad_id = int(callback.data.split("_")[1])
    phone = session.query(Phone).filter(Phone.id == ad_id, Phone.user_id == callback.from_user.id).first()

    if phone:
        session.delete(phone)
        session.commit()
        await callback.message.answer("✅ Объявление удалено!")
        await callback.message.delete()
    else:
        await callback.answer("❌ Ошибка: объявление не найдено или не принадлежит вам.", show_alert=True)

# 3. FSM для редактирования объявления
class EditState(StatesGroup):
    waiting_for_field = State()
    waiting_for_value = State()

@router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_ad(callback: CallbackQuery, state: FSMContext):
    ad_id = int(callback.data.split("_")[1])
    await state.update_data(ad_id=ad_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💰 Цена", callback_data="edit_price")],
            [InlineKeyboardButton(text="📌 Описание", callback_data="edit_description")]
        ]
    )

    await callback.message.answer("Выберите, что изменить:", reply_markup=keyboard)
    await state.set_state(EditState.waiting_for_field)

@router.callback_query(EditState.waiting_for_field)
async def edit_field(callback: CallbackQuery, state: FSMContext):
    field = callback.data.split("_")[1]
    await state.update_data(field=field)

    await callback.message.answer(f"Введите новое значение для {field}:")
    await state.set_state(EditState.waiting_for_value)

@router.message(EditState.waiting_for_value)
async def save_edit(message: types.Message, state: FSMContext, session: Session = get_db()):
    data = await state.get_data()
    ad_id, field, value = data["ad_id"], data["field"], message.text

    phone = session.query(Phone).filter(Phone.id == ad_id).first()
    if phone:
        setattr(phone, field, value)
        session.commit()
        await message.answer("✅ Объявление обновлено!")
    else:
        await message.answer("❌ Ошибка: объявление не найдено.")

    await state.clear()
