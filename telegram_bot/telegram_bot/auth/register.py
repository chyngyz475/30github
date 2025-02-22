import aiohttp
import random
import string
from config import HEADERS
from utils.proxy_handler import get_proxy
from utils.captcha_solver import solve_captcha
from utils.storage import save_account

REGISTER_URL = "https://egbs.live/api/register"

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "mail.ru", "protonmail.com"]
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@" + random.choice(domains)

async def register_new_account():
    email = generate_random_email()
    password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
    proxy = get_proxy()

    async with aiohttp.ClientSession() as session:
        async with session.get("https://egbs.live/register", headers=HEADERS, proxy=proxy) as response:
            html = await response.text()

            captcha_img = "URL_КАРТИНКИ_КАПЧИ"  # Парсим URL капчи
            captcha_solution = await solve_captcha(captcha_img)

            data = {
                "email": email,
                "password": password,
                "captcha": captcha_solution
            }

            async with session.post(REGISTER_URL, json=data, headers=HEADERS, proxy=proxy) as register_response:
                if register_response.status == 200:
                    save_account(email, password)
                    return {"email": email, "password": password, "status": "Успешная регистрация"}
                else:
                    return {"error": f"Ошибка регистрации: {register_response.status}"}
