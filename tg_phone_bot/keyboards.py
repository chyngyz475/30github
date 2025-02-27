from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Список телефонов"), KeyboardButton(text="➕ Добавить телефон")],
        [KeyboardButton(text="🔎 Поиск")]
    ],
    resize_keyboard=True
)

