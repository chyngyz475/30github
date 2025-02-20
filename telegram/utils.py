 
# utils.py

import random
import time
from config import PROXY
import requests

# Получение случайного прокси
def get_proxy():
    return random.choice([PROXY])

# Решение капчи с использованием 2Captcha или CapMonster
def solve_captcha(api_key, url):
    # Пример для 2Captcha
    payload = {
        "key": api_key,
        "method": "userrecaptcha",
        "googlekey": "sitekey",  # Этот ключ нужно брать с сайта
        "pageurl": url,
    }
    
    response = requests.post('http://2captcha.com/in.php', data=payload)
    captcha_id = response.text.split('|')[1]
    
    time.sleep(20)  # Ждём, пока капча будет решена
    
    result_payload = {
        "key": api_key,
        "action": "get",
        "id": captcha_id,
    }
    
    result = requests.post('http://2captcha.com/res.php', data=result_payload)
    
    if "OK" in result.text:
        return result.text.split('|')[1]
    else:
        return None
