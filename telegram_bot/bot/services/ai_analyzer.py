import openai

class AIService:
    def __init__(self, api_key):
        openai.api_key = api_key

    def analyze_content(self, content):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following content for payment data: {content}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
