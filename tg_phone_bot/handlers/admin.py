from aiogram import Router, types, F
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
async def cmd_add(message: types.Message, state: FSMContext):
    if message.from_user.id != config.ADMIN_ID:
        return await message.answer("У вас нет прав для добавления объявлений!")
    
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
    await state.update_data(price=int(message.text))
    await state.set_state(AddPhone.battery)
    await message.answer("Введите остаток батареи (в %):")

@router.message(AddPhone.battery)
async def add_battery(message: types.Message, state: FSMContext):
    await state.update_data(battery=int(message.text))
    await state.set_state(AddPhone.condition)
    await message.answer("Введите состояние (новый / б/у):")

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

@router.message(AddPhone.photos, F.photo)
async def add_photos(message: types.Message, state: FSMContext, session: Session = get_db()):
    data = await state.get_data()
    photos = [photo.file_id for photo in message.photo]

    new_phone = Phone(
        admin_id=message.from_user.id,
        brand=data["brand"],
        model=data["model"],
        price=data["price"],
        battery=data["battery"],
        condition=data["condition"],
        description=data["description"],
        photos=photos,
    )

    session.add(new_phone)
    session.commit()

    await state.clear()
    await message.answer("Телефон успешно добавлен!")
