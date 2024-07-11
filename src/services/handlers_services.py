from whatsapp_chatbot_python import Notification
import re
import requests
from settings import CRM_TOKEN, CRM_URL
from bot_logger import init_logger


logger = init_logger(__name__)


def parse_notification(notification: Notification):
    sender_chat_id = notification.event["senderData"]["chatId"]
    sender_phone_number = "+" + re.sub("@c.us", "", sender_chat_id)
    message_text = notification.event["messageData"]["extendedTextMessageData"]["text"]
    return {"sender_phone_number": sender_phone_number, "text": message_text}


def create_five_points_feedback(notification: Notification) -> None:
    result = parse_notification(notification)
    phone_number = result["sender_phone_number"]
    text = result["text"]
    status = "ok"
    feedback = get_feedback(phone_number)
    data = change_feedback_data(feedback, status, text)
    send_put_request_to_crm(data)


def get_feedback(phone_number: str):
    url = f"{CRM_URL}/api/feedback/"
    headers = {"Authorization": f"Token {CRM_TOKEN}"}
    params = {"phone": phone_number, "results[]": "message_send"}
    response = requests.get(url=url, headers=headers, params=params)
    data = response.json()
    result = data.get("results")[0]
    return result


def change_feedback_data(feedback, status, text):
    data = {
        "id": feedback["id"],
        "order": feedback["order"]["id"],
        "result_id": status,
        "comment": text
    }
    return data


def send_put_request_to_crm(data):
    feedback_id = data.get("id")
    url = f"{CRM_URL}/api/feedback/{feedback_id}/"
    headers = {"Authorization": f"Token {CRM_TOKEN}"}
    response = requests.put(
        url=url, headers=headers, data=data
    )


def create_middle_grade_feedback(notification: Notification) -> None:
    result = parse_notification(notification)
    phone_number = result["sender_phone_number"]
    text = result["text"]
    status = "nok"
    feedback = get_feedback(phone_number)
    data = change_feedback_data(feedback, status, text)
    send_put_request_to_crm(data)


def create_low_grade_feedback(notification: Notification) -> None:
    result = parse_notification(notification)
    phone_number = result["sender_phone_number"]
    text = result["text"]
    status = "critical"
    feedback = get_feedback(phone_number)
    data = change_feedback_data(feedback, status, text)
    send_put_request_to_crm(data)