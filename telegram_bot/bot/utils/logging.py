import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Логирование ошибок
try:
    # Парсинг или другая логика
    pass
except Exception as e:
    logger.error(f"Ошибка: {str(e)}")
