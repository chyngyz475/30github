import hashlib
import os
import json

CACHE_DIR = 'data/cache/'

class CacheService:
    def __init__(self):
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

    def get_cache_key(self, url):
        return hashlib.md5(url.encode()).hexdigest()

    def cache_exists(self, url):
        return os.path.exists(self.get_cache_path(url))

    def get_cache(self, url):
        with open(self.get_cache_path(url), 'r') as f:
            return json.load(f)

    def save_cache(self, url, data):
        with open(self.get_cache_path(url), 'w') as f:
            json.dump(data, f)

    def get_cache_path(self, url):
        return os.path.join(CACHE_DIR, self.get_cache_key(url) + '.json')
