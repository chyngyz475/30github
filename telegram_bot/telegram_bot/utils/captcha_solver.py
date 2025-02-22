import aiohttp
from config import CAPTCHA_API_KEY

async def solve_captcha(captcha_url):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://2captcha.com/in.php",
            data={"key": CAPTCHA_API_KEY, "method": "base64", "body": captcha_url}
        ) as response:
            result = await response.text()
            return result.split("|")[1] if "OK" in result else None
