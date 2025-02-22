import os
from dotenv import load_dotenv

# Загружаем .env файл
load_dotenv()

# Получаем токен из окружения
TOKEN = os.getenv("TOKEN")  # Используем переменную из .env файла

# Получаем список прокси
PROXY_LIST = os.getenv("PROXY_LIST", "").split(",")
CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY")
HEADERS = {"User-Agent": "Mozilla/5.0"}
JSON_DB_PATH = "data.json"

# Проверим, что токен был правильно загружен
if TOKEN is None:
    raise ValueError("Token not found. Please check the .env file.")
