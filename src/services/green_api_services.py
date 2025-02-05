from settings import (
    ID_INSTANCE,
    API_TOKEN_INSTANCE,
    OPERATOR_PHONE_NUMBER
)
from whatsapp_api_client_python.API import GreenApi
from whatsapp_api_client_python.response import Response


class GreenAPIManager:
    def __init__(self):
        self.instance_id = ID_INSTANCE
        self.instance_token = API_TOKEN_INSTANCE
        self.operator_whatsapp_id = f"{OPERATOR_PHONE_NUMBER}@c.us"

    def forward_message(self, message_id: str, sender_id: int) -> Response:
        api = GreenApi(self.instance_id, self.instance_token)
        response = api.sending.forwardMessages(
            chatId=self.operator_whatsapp_id,
            chatIdFrom=sender_id,
            messages=[message_id]
        )
        return response
