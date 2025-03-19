import asyncio
import logging
import signal
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from config import TOKEN
from database import init_db
from handlers import admin, user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(admin.router)
dp.include_router(user.router)

async def on_startup():
    logger.info("Инициализация базы данных...")
    init_db()
    logger.info("Бот запущен!")

async def shutdown(signal, dp):
    logger.info(f"Получен сигнал {signal}, завершение работы...")
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.session.close()

async def main():
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(sig, dp)))
    asyncio.run(main())