 
# scraper.py

import requests
import json
from bs4 import BeautifulSoup
from utils import solve_captcha, get_proxy
from config import CAPTCHA_API_KEY, PROXY
from models import Database

# Инициализация базы данных
db = Database('database.db')
db.create_table()

# Функция для получения данных с сайта
def fetch_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    proxy = get_proxy()

    # Решение капчи
    captcha_solution = None
    if "captcha" in url:  # Пример, как можно проверить на наличие капчи
        captcha_solution = solve_captcha(CAPTCHA_API_KEY, url)

    if captcha_solution:
        headers['Captcha-Solution'] = captcha_solution

    response = requests.get(url, headers=headers, proxies=proxy, timeout=30)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Пример парсинга данных
        card_numbers = []  # Пример для карт
        phone_numbers = []  # Пример для телефонов
        
        for card in soup.find_all('div', {'class': 'card-number'}):  # Пример класса
            card_numbers.append(card.get_text())
        for phone in soup.find_all('div', {'class': 'phone-number'}):  # Пример класса
            phone_numbers.append(phone.get_text())
        
        data = {
            "url": url,
            "card_numbers": card_numbers,
            "phone_numbers": phone_numbers
        }
        
        # Проверка на дубликаты
        if not db.is_duplicate(url):
            db.save_data(data)
            print(f"Данные для {url} успешно собраны и сохранены в базу.")
        else:
            print(f"Дублированные данные для {url}, не добавлены.")
    else:
        print(f"Ошибка доступа к сайту: {url}")
