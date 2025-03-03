import os
import io
from PIL import Image
from aiogram import Router, Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session
from database import get_db
from models import Phone
import config

router = Router()

class AddPhone(StatesGroup):
    brand = State()
    model = State()
    price = State()
    battery = State()
    condition = State()
    description = State()
    photos = State()

# Команда /add
@router.message(Command("add"))
@router.message(lambda message: message.text == "➕ Добавить телефон")
async def cmd_add(message: types.Message, state: FSMContext):
    if message.from_user.id != config.ADMIN_ID:
        return await message.answer("🚫 У вас нет прав для добавления объявлений!")
    
    await state.set_state(AddPhone.brand)
    await message.answer("Введите бренд телефона (например, Apple, Samsung):")

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
        await state.set_state(AddPhone.battery)
        await message.answer("Введите остаток батареи (в %):")
    except ValueError:
        await message.answer("Ошибка! Введите число.")

@router.message(AddPhone.battery)
async def add_battery(message: types.Message, state: FSMContext):
    try:
        battery = int(message.text)
        await state.update_data(battery=battery)
        await state.set_state(AddPhone.condition)
        await message.answer("Введите состояние (новый / б/у):")
    except ValueError:
        await message.answer("Ошибка! Введите число.")

@router.message(AddPhone.condition)
async def add_condition(message: types.Message, state: FSMContext):
    await state.update_data(condition=message.text)
    await state.set_state(AddPhone.description)
    await message.answer("Введите описание телефона:")

@router.message(AddPhone.description)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddPhone.photos)
    await message.answer("Загрузите 1-3 фото телефона:")

# Функция обработки фото
async def save_photo(bot: Bot, file_id: str) -> str:
    """Скачивает, изменяет размер и сохраняет фото в папку media"""
    file = await bot.download(file_id)
    image = Image.open(file)
    image = image.resize((800, 800), Image.ANTIALIAS)

    # Создаем папку media, если её нет
    os.makedirs("media", exist_ok=True)

    # Сохранение файла
    photo_path = f"media/{file_id}.jpg"
    with open(photo_path, "wb") as img_file:
        image.save(img_file, format="JPEG")

    return photo_path

@router.message(AddPhone.photos, lambda message: message.photo)
async def add_photos(message: types.Message, state: FSMContext, bot: Bot):
    """Обрабатывает загрузку фото и сохраняет данные в БД"""
    data = await state.get_data()
    user_photos = data.get("photos", [])

    # Ограничение по количеству фото (не больше 3)
    if len(user_photos) >= 3:
        return await message.answer("❌ Можно загрузить не более 3-х фото!")

    file_id = message.photo[-1].file_id  # Берем самое большое фото
    photo_path = await save_photo(bot, file_id)

    # Обновляем список фото
    user_photos.append(photo_path)
    await state.update_data(photos=user_photos)

    # Если уже 3 фото, сохраняем в БД
    if len(user_photos) == 3:
        await save_phone_data(message, state)
    else:
        await message.answer(f"✅ Фото добавлено ({len(user_photos)}/3). Загрузите еще или отправьте /done для сохранения.")

@router.message(Command("done"))
async def finish_adding_photos(message: types.Message, state: FSMContext):
    """Завершает процесс добавления фото"""
    data = await state.get_data()
    user_photos = data.get("photos", [])

    if not user_photos:
        return await message.answer("❌ Вы не загрузили ни одного фото. Пожалуйста, загрузите хотя бы одно!")

    await save_phone_data(message, state)

async def save_phone_data(message: types.Message, state: FSMContext):
    """Сохраняет объявление в базу данных"""
    data = await state.get_data()

    session = get_db()  # Открываем сессию
    try:
        new_phone = Phone(
            admin_id=message.from_user.id,
            brand=data["brand"],
            model=data["model"],
            price=data["price"],
            battery=data["battery"],
            condition=data["condition"],
            description=data["description"],
            photos=data["photos"],
        )

        session.add(new_phone)
        session.commit()
        await state.clear()
        await message.answer("✅ Телефон успешно добавлен!")
    finally:
        session.close()  # Закрываем сессию

