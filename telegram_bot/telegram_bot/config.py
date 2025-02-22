import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PROXY_LIST = os.getenv("PROXY_LIST", "").split(",")
CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY")
HEADERS = {"User-Agent": "Mozilla/5.0"}
JSON_DB_PATH = "data.json"
