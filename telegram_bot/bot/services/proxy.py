class ProxyService:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    def get_proxy(self):
        # Выбор случайного прокси из списка
        return {'server': f'http://{self.proxy_list[0]}'}

    def set_proxy(self, page):
        proxy = self.get_proxy()
        page.context.set_proxy(proxy)
