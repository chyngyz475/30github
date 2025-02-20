from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging

API_TOKEN = '7415359822:AAF51xrFN4y1owp2OxDmOTKtU0JWMmu4QVI'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправьте ссылку на сайт для парсинга.")

@dp.message_handler()
async def handle_link(message: types.Message):
    url = message.text.strip()

    # Проверка кэша
    cache_service = CacheService()
    if cache_service.cache_exists(url):
        data = cache_service.get_cache(url)
    else:
        parser = SiteParser(url)
        data = parser.parse()
        cache_service.save_cache(url, data)

    # Формирование HTML-ответа
    response_html = f"<b>Номера карт:</b> {', '.join(data[0])}\n"
    response_html += f"<b>Номера телефонов:</b> {', '.join(data[1])}\n"
    response_html += f"<b>P2P данные:</b> {', '.join(data[2])}"

    await message.reply(response_html, parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
