import unittest
from parser import CardParser

class TestCardParser(unittest.TestCase):
    def test_parse(self):
        url = "https://example.com"
        parser = CardParser()
        result = parser.parse(url)
        self.assertTrue(len(result) > 0, "Номера карт должны быть извлечены")
