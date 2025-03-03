from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Запускаем браузер
driver = webdriver.Chrome()

# Открываем WhatsApp Web
driver.get("https://web.whatsapp.com")
input("Отсканируйте QR-код, затем нажмите Enter...")

# Указываем контакт или группу
target_name = "Имя_контакта_или_группы"
message = "Привет! Я бот!"

# Ищем контакт
search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
search_box.send_keys(target_name)
search_box.send_keys(Keys.ENTER)
time.sleep(2)

# Отправляем сообщение
message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
message_box.send_keys(message)
message_box.send_keys(Keys.ENTER)

print("Сообщение отправлено!")
time.sleep(5)
driver.quit()

# Закрываем браузер