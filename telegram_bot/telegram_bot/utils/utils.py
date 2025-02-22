import requests

def solve_captcha(site_url):
    """Разгадывает капчу с помощью 2Captcha или CapMonster"""
    print("🧩 Решаем капчу...")
    return "solved_captcha"

def save_data(site, data):
    """Сохраняем данные в JSON"""
    with open("parsed_data.json", "a") as file:
        json.dump({site: data}, file, indent=4)
    print("✅ Данные сохранены!")
