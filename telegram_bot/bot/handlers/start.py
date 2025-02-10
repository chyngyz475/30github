from aiogram import types

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправьте ссылку на сайт для парсинга.")

@dp.message_handler()
async def handle_link(message: types.Message):
    url = message.text.strip()
    
    # Проверка и парсинг
    try:
        # Парсинг данных с сайта
        card_numbers, phone_numbers = parse_site(url)
        
        # Формирование ответа
        response = f"Номера карт:\n{', '.join(card_numbers)}\n"
        response += f"Номера телефонов:\n{', '.join(phone_numbers)}"
        
        # Отправка данных пользователю
        await message.reply(response)
    
    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")
