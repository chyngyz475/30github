from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Запускаем браузер
driver = webdriver.Chrome()

# Открываем WhatsApp Web
driver.get("https://web.whatsapp.com")
input("Отсканируйте QR-код, затем нажмите Enter...")

def send_reply(contact_name, message):
    """Отправка ответа пользователю."""
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    search_box.send_keys(contact_name)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)

    message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    message_box.send_keys(message)
    message_box.send_keys(Keys.ENTER)
    print(f"Ответ отправлен: {message}")

print("Бот запущен и ожидает сообщения...")

while True:
    try:
        # Ищем все входящие непрочитанные сообщения
        unread_messages = driver.find_elements(By.XPATH, "//span[@class='_2nY6U']")

        for message in unread_messages:
            message.click()
            time.sleep(2)

            # Получаем имя контакта
            contact_name = driver.find_element(By.XPATH, "//header//span").text
            print(f"Новое сообщение от {contact_name}")

            # Отвечаем на сообщение
            send_reply(contact_name, "Привет! Я бот. Как я могу помочь?")

        time.sleep(5)  # Проверять новые сообщения каждые 5 секунд

    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
