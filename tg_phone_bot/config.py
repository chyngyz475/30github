import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID") 
DB_URL = os.getenv("DB_URL") 