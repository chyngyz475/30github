# bot.py

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.log import logging
from aiogram.utils import executor
from scraper import fetch_data
from config import TELEGRAM_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Команда старт
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.reply("Привет! Отправь ссылку, чтобы получить данные.")

# Обработчик для всех сообщений с текстом
@dp.message_handler(lambda message: not message.text.startswith('/'))
async def handle_link(message: types.Message):
    url = message.text
    fetch_data(url)
    await message.reply(f"Обработка ссылки {url} завершена.")

# Главная функция, запускающая бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
