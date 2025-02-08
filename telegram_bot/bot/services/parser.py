from playwright.sync_api import sync_playwright
import re

class SiteParser:
    def __init__(self, url):
        self.url = url

    def parse(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.url)
            
            # Обход защиты Cloudflare с помощью Stealth
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            # Ждем, чтобы сайт загрузился
            page.wait_for_timeout(2000)

            content = page.content()

            # Извлечение данных с помощью регулярных выражений
            card_numbers = self.extract_card_numbers(content)
            phone_numbers = self.extract_phone_numbers(content)
            p2p_data = self.extract_p2p_data(content)

            browser.close()

        return card_numbers, phone_numbers, p2p_data

    def extract_card_numbers(self, content):
        # Пример регулярного выражения для поиска номеров карт
        return re.findall(r'\b\d{4} \d{4} \d{4} \d{4}\b', content)

    def extract_phone_numbers(self, content):
        # Пример регулярного выражения для поиска номеров телефонов
        return re.findall(r'\+?\d{1,4}?[\s.-]?\(?\d{1,4}?\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}', content)

    def extract_p2p_data(self, content):
        # Пример для извлечения информации о P2P
        return re.findall(r'P2P.*?(\d{4} \d{4} \d{4} \d{4})', content)
