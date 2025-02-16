import re
import asyncio
from playwright.async_api import async_playwright
from bot.services.cache import get_cached_data, set_cache_data
from bot.services.proxy import get_proxy
from bot.utils.logging import logger

async def parse_website(url: str):
    """Парсит страницу и ищет платежные данные."""
    # Проверяем кэш
    cached_result = await get_cached_data(url)
    if cached_result:
        logger.info(f"Данные взяты из кэша для {url}")
        return cached_result.split("\n")

    proxy = get_proxy()
    logger.info(f"Используем прокси: {proxy}" if proxy else "Запрос без прокси")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(proxy={"server": proxy} if proxy else None)
        page = a
