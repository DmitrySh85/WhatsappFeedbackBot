import json

from openai import OpenAI

from bot_logger import init_logger
from settings import DEEPSEEK_API_TOKEN
from .types import Result


class DeepseekAPIManager:

    def __init__(self):
        self.client = OpenAI(api_key=DEEPSEEK_API_TOKEN, base_url="https://api.deepseek.com")

    def send_recognition_request(
            self,
            text: str,
    ) -> Result | None:
        prompt = (
            "Ты анализируешь отзывы клиентов для сети автосервисов 'Геликон'.\n"
            "Инструкции:\n"
            "1. Если сообщение содержит оценку сервиса (цифру от 1 до 5, словами или эмодзи) - верни JSON с полями 'grade' и 'description'\n"
            "2. Если оценки нет (приветствия, вопросы, благодарности без оценки) - верни JSON только с 'description'\n"
            "3. Формат ответа ТОЧНО как указано, без лишних символов\n\n"
            "Примеры:\n"
            "Вход: '5 звёзд' → Выход: {'grade': '5', 'description': 'Клиент явно указал высшую оценку'}\n"
            "Вход: 'спасибо' → Выход: {'description': 'Сообщение не содержало оценки качества работы сервиса'}\n\n"
            "Текущее сообщение:"
        )
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            stream=False
        )
        return json.loads(response.choices[0].message.content)