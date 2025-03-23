from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class EditPhone(StatesGroup):
    waiting_for_field = State()
    waiting_for_value = State()

@router.message(Command("edit"))
async def edit_phone(message: types.Message, state: FSMContext):
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("⚠ Укажите ID телефона, который хотите редактировать.\nПример: `/edit 123`", parse_mode="Markdown")
    phone_id = args[1]
    session: Session = get_db()  # Ошибка здесь!
    phone = session.query(Phone).filter_by(id=phone_id, admin_id=message.from_user.id).first()
    
    if not phone:
        session.close()
        return await message.answer("🚫 Телефон не найден или у вас нет прав на его редактирование.")

    await state.update_data(phone_id=phone_id)
    await state.set_state(EditPhone.waiting_for_field)
    await message.answer("Что хотите изменить? Введите:\n\n🔹 `brand` – Бренд\n🔹 `model` – Модель\n🔹 `price` – Цена\n🔹 `battery` – Батарея\n🔹 `condition` – Состояние\n🔹 `description` – Описание\n🔹 `photo` – Фото", parse_mode="Markdown")

@router.message(EditPhone.waiting_for_field)
async def edit_field(message: types.Message, state: FSMContext):
    field = message.text.lower()
    allowed_fields = ["brand", "model", "price", "battery", "condition", "description", "photo"]

    if field not in allowed_fields:
        return await message.answer("🚫 Неверное поле. Выберите одно из предложенных выше.")

    await state.update_data(field=field)
    
    if field == "photo":
        await state.set_state(EditPhone.waiting_for_value)
        return await message.answer("📸 Загрузите новую фотографию.")

    await state.set_state(EditPhone.waiting_for_value)
    await message.answer(f"Введите новое значение для `{field}`:", parse_mode="Markdown")

@router.message(EditPhone.waiting_for_value, lambda message: not message.photo)
async def edit_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_id = data["phone_id"]
    field = data["field"]
    
    session: Session = get_db()
    phone = session.query(Phone).filter_by(id=phone_id).first()

    setattr(phone, field, message.text)
    session.commit()
    session.close()

    await state.clear()
    await message.answer(f"✅ Поле `{field}` успешно обновлено!", parse_mode="Markdown")

@router.message(EditPhone.waiting_for_value, lambda message: message.photo)
async def edit_photo(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    phone_id = data["phone_id"]

    file_id = message.photo[-1].file_id
    file = await bot.download(file_id)
    
    image = Image.open(file)
    image = image.resize((800, 800), Image.ANTIALIAS)

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG")

    photo_path = f"media/{file_id}.jpg"
    with open(photo_path, "wb") as img_file:
        img_file.write(img_byte_arr.getvalue())

    session: Session = get_db()
    phone = session.query(Phone).filter_by(id=phone_id).first()
    phone.photos = [photo_path]
    session.commit()
    session.close()

    await state.clear()
    await message.answer("✅ Фото успешно обновлено!")
