import requests
import json

from bot_logger import init_logger
from .types import Response, Result
from settings import YANDEX_CATALOG_ID, YANDEX_API_TOKEN


logger = init_logger(__name__)


class YandexAPIManager:  

    def send_recognition_request(
            self,
            text: str,
    ) -> Result | None:
        print("ENTER THE METHOD")
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        prompt = (
            "Мы сеть автосервисов Геликон. Мы находимся в Нижнем Новгороде, Москве и Алматы."
            "Мы пересылаем тебе сообщение от клиента."
            "Сообщение может содержать в себе оценку качества работы автосервиса,"
            "или не содержать полезной информации."
            "Короткие ответы наподобии 'Понял', 'Спасибо', тоже не несут полезной информации"
            "Расшифруй оценку работы сервиса, которую дал клиент по пятибальной шкале."
            "Верни ответ в виде объекта JSON вида: "
            "{'grade': '5', 'description': 'Твое объяснение почему ты выбрал этот результат'}"
            "Eсли сообщение не содержит оценки работы сервиса, ответь в формате"
            "{'description': 'Сообщение не содержало оценки качества работы сервиса'}(не указывая grade)"
        )
        payload = {
            "modelUri": f"gpt://{YANDEX_CATALOG_ID}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0,
                "maxTokens": "500",
                "reasoningOptions": {
                "mode": "ENABLED_HIDDEN"
                }
            },
            "messages": [
                {
                    "role": "system",
                    "text": prompt,               
                },
                {
                    "role": "user",
                    "text": text
                }
            ],
            "jsonObject": False,
                }
        headers = {"Authorization": f"Api-Key {YANDEX_API_TOKEN}"}
        response = requests.post(
            url,
            json=payload,
            headers=headers
        )
        try:
            data = response.json()
        except Exception as e:
            logger.debug(e)
            return
        result = self._parse_ai_answer(data)
        alternatives = data.get("result", {}).get("alternatives", [])
        if alternatives:
            content = alternatives[0].get("message",{}).get("text").strip("```")
            result = json.loads(content)
            if type(result) == list and len(result) > 0:
                result = result[0]
            logger.info(result)
            return result   
        return result     

    def _parse_ai_answer(self, data: Response) -> Result:
        alternatives = data.get("result", {}).get("alternatives", [])
        if alternatives:
            content = alternatives[0].get("message",{}).get("text").strip("```")
            result = json.loads(content)
            logger.info(result)
            return result 