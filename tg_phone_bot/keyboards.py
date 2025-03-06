from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import config

def get_main_menu(user_id: int):
    """Генерация клавиатуры в зависимости от роли пользователя."""
    
    keyboard = []

    if user_id == config.ADMIN_ID:  # Проверяем, является ли пользователь админом
        keyboard.append([KeyboardButton(text="📋 Список телефонов")])
        keyboard.append([KeyboardButton(text="➕ Добавить телефон")])

    keyboard.append([KeyboardButton(text="🔎 Поиск")])
    keyboard.append([KeyboardButton(text="🔑 Админ")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
