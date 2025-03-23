from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_admin_menu():
    keyboard = [
        [KeyboardButton(text="➕ Добавить телефон")],
        [KeyboardButton(text="📋 Мои объявления")],
        [KeyboardButton(text="📩 Заявки")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_main_menu():
    keyboard = [
        [KeyboardButton(text="📱 Список телефонов")],
        [KeyboardButton(text="ℹ Информация")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)