import aiohttp
from bs4 import BeautifulSoup
from config import HEADERS
from utils.captcha_solver import solve_captcha
from utils.proxy_handler import get_proxy

async def parse_egbs(url):
    proxy = get_proxy()
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, proxy=proxy) as response:
            if response.status != 200:
                return {"error": f"Ошибка: {response.status}"}
            
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            
            captcha = soup.find("img", {"class": "captcha"})
            if captcha:
                solved_captcha = await solve_captcha(captcha["src"])
                # Применяем решение капчи и повторяем запрос...

            phone_numbers = [el.text for el in soup.find_all("div", class_="phone-number")]
            return {"phones": phone_numbers}
