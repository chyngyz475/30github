from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from sqlalchemy.orm import Session
from database import get_db
from models import Phone, Request, User
from keyboards import get_main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    with next(get_db()) as session:
        user = session.query(User).filter_by(id=message.from_user.id).first()
        if not user:
            user = User(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                username=message.from_user.username,
                role="user"
            )
            session.add(user)
            session.commit()
    await message.answer("👋 Добро пожаловать! Выберите действие:", reply_markup=get_main_menu())

@router.message(lambda message: message.text == "📱 Список телефонов")
async def list_phones_handler(message: types.Message):
    await list_phones(message)
    with next(get_db()) as session:
        phones = session.query(Phone).filter(Phone.status == "active").all()
        if not phones:
            await message.answer("📭 Объявлений пока нет!")
            return
        for phone in phones:
            caption = (
                f"<b>📱 {phone.brand} {phone.model}</b>\n"
                f"💰 Цена: {phone.price} руб.\n"
                f"🔋 Батарея: {phone.battery or 'N/A'}%\n"
                f"🛠 Состояние: {phone.condition}\n"
                f"📌 Описание: {phone.description or 'Нет описания'}"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Забронировать", callback_data=f"reserve_{phone.id}")],
                [InlineKeyboardButton(text="📩 Написать продавцу", callback_data=f"chat_{phone.admin_id}")]
            ])
            if phone.photos:
                await message.answer_photo(phone.photos[0], caption=caption, reply_markup=keyboard)
            else:
                await message.answer(caption, reply_markup=keyboard)


async def list_phones(message: types.Message, page: int = 0):
    ITEMS_PER_PAGE = 5
    with next(get_db()) as session:
        phones = session.query(Phone).filter(Phone.status == "active").offset(page * ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE).all()
        total = session.query(Phone).filter(Phone.status == "active").count()
        if not phones:
            await message.answer("📭 Объявлений пока нет!")
            return
        for phone in phones:
            caption = f"<b>📱 {phone.brand} {phone.model}</b>\n..."
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Забронировать", callback_data=f"reserve_{phone.id}")],
                [InlineKeyboardButton(text="📩 Написать продавцу", callback_data=f"chat_{phone.admin_id}")]
            ])
            if total > ITEMS_PER_PAGE:
                nav_buttons = []
                if page > 0:
                    nav_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=f"page_{page-1}"))
                if (page + 1) * ITEMS_PER_PAGE < total:
                    nav_buttons.append(InlineKeyboardButton(text="Далее ➡", callback_data=f"page_{page+1}"))
                keyboard.inline_keyboard.append(nav_buttons)
            await message.answer_photo(phone.photos[0], caption=caption, reply_markup=keyboard) if phone.photos else await message.answer(caption, reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("page_"))
async def paginate(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    await list_phones(callback.message, page)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("reserve_"))
async def reserve_phone(callback: CallbackQuery):
    phone_id = int(callback.data.split("_")[1])
    with next(get_db()) as session:
        phone = session.query(Phone).filter_by(id=phone_id, status="active").first()
        if phone:
            phone.status = "reserved"
            request = Request(phone_id=phone_id, user_id=callback.from_user.id)
            session.add(request)
            session.commit()
            await callback.message.answer("✅ Заявка принята! Ждите ответа менеджера.")
            # Уведомление админа
            await callback.bot.send_message(
                phone.admin_id,
                f"📩 Новая заявка на телефон: {phone.brand} {phone.model} (ID: {phone_id})"
            )
        else:
            await callback.answer("❌ Телефон уже забронирован или продан.", show_alert=True)
    await callback.answer()

@router.message(lambda message: message.text == "ℹ Информация")
async def show_info(message: types.Message):
    info_text = (
        "📬 **Информация о доставке и контакты**\n"
        "Доставка: по всей России через СДЭК или Почту России.\n"
        "Срок: 3-7 дней.\n"
        "Контакты: @PhoneBotSupport\n"
        "Оплата: перевод на карту после подтверждения заказа."
    )
    await message.answer(info_text)



# Добавляем в начало файла
chat_sessions = {}  # Хранилище активных чатов: {user_id: admin_id}

@router.callback_query(lambda c: c.data.startswith("chat_"))
async def start_chat(callback: CallbackQuery, bot: Bot):
    admin_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    # Проверяем, не занят ли пользователь другим чатом
    if user_id in chat_sessions:
        await callback.answer("❌ Вы уже в чате!", show_alert=True)
        return

    chat_sessions[user_id] = admin_id
    chat_sessions[admin_id] = user_id  # Двусторонняя связь

    await callback.message.answer("✅ Вы начали чат с продавцом. Напишите сообщение:")
    await bot.send_message(admin_id, f"📩 Пользователь @{callback.from_user.username or user_id} хочет связаться с вами!")
    await callback.answer()

@router.message(lambda message: message.from_user.id in chat_sessions)
async def forward_message(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    recipient_id = chat_sessions[user_id]
    await bot.send_message(recipient_id, f"💬 @{message.from_user.username or user_id}: {message.text}")

@router.message(Command("end_chat"))
async def end_chat(message: types.Message):
    user_id = message.from_user.id
    if user_id in chat_sessions:
        recipient_id = chat_sessions.pop(user_id)
        chat_sessions.pop(recipient_id, None)
        await message.answer("✅ Чат завершен.")
        await message.bot.send_message(recipient_id, "❌ Чат завершен пользователем.")
    else:
        await message.answer("🚫 Вы не в чате.")