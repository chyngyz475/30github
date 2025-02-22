# casino_parser.py

import json
import random
import time
import requests
from bs4 import BeautifulSoup
from config import PROXIES, CAPTCHA_API_KEY, HEADERS
from utils import solve_captcha, save_data

class CasinoParser:
    def __init__(self, site_url):
        self.site_url = site_url
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.proxy = random.choice(PROXIES) if PROXIES else None
        self.session.proxies.update({'http': self.proxy, 'https': self.proxy})

    def register(self):
        """Регистрируем аккаунт на казино"""
        email = f"user{random.randint(1000,9999)}@example.com"
        password = "CasinoPassword123!"
        data = {"email": email, "password": password}
        
        response = self.session.post(f"{self.site_url}/register", data=data)
        if response.status_code == 200:
            print(f"✅ Успешно зарегистрирован: {email}")
            return email, password
        else:
            print("❌ Ошибка регистрации", response.text)
            return None, None

    def login(self, email, password):
        """Логинимся в казино"""
        data = {"email": email, "password": password}
        response = self.session.post(f"{self.site_url}/login", data=data)

        if "captcha" in response.text:
            captcha_solution = solve_captcha(self.site_url)
            data["captcha"] = captcha_solution
            response = self.session.post(f"{self.site_url}/login", data=data)

        if response.status_code == 200:
            print(f"✅ Успешно вошли: {email}")
            return True
        else:
            print("❌ Ошибка входа", response.text)
            return False

    def go_to_deposit_page(self):
        """Переход на страницу пополнения и парсинг"""
        response = self.session.get(f"{self.site_url}/deposit")
        if response.status_code != 200:
            print("❌ Ошибка перехода на страницу пополнения")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        numbers = [num.text for num in soup.find_all(class_="phone-number")]
        cards = [card.text for card in soup.find_all(class_="card-number")]

        return {"phones": numbers, "cards": cards}

    def parse_casino(self):
        """Основной метод"""
        email, password = self.register()
        if not email:
            return None

        if not self.login(email, password):
            return None

        deposit_data = self.go_to_deposit_page()
        if deposit_data:
            print(f"📊 Найденные данные: {deposit_data}")
            save_data(self.site_url, deposit_data)
        else:
            print("❌ Данные не найдены")

if __name__ == "__main__":
    parser = CasinoParser("https://egbs.live/")
    parser.parse_casino()
