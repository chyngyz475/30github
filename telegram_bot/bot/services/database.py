import requests

class P2PService:
    def __init__(self, api_url):
        self.api_url = api_url

    def verify_p2p_data(self, card_number):
        response = requests.get(f'{self.api_url}/verify', params={'card_number': card_number})
        return response.json() if response.status_code == 200 else None
