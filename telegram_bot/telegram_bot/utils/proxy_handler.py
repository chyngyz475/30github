import random
from config import PROXY_LIST

def get_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST else None
