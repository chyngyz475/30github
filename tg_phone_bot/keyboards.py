from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Список телефонов"), KeyboardButton(text="➕ Добавить телефон")],
    ],
    resize_keyboard=True
)
