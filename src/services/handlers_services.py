from whatsapp_chatbot_python import Notification
import re
import requests
from settings import CRM_TOKEN, CRM_URL
from bot_logger import init_logger
from requests.exceptions import ConnectionError


logger = init_logger(__name__)


class CRMAPIError(Exception):
    """Error during API request to CRM"""


class GreenAPIError(Exception):
    """Error from GreenAPI library"""


def parse_notification(notification: Notification):
    sender = notification.get_sender()
    if sender:
        sender_phone_number = "+" + re.sub("@c.us", "", sender)
    else:
        raise GreenAPIError("Sender not found")
    message_text = notification.get_message_text()
    return {"sender_phone_number": sender_phone_number, "text": message_text}


def create_five_points_feedback(notification: Notification) -> None:
    try:
        result = parse_notification(notification)
    except GreenAPIError as e:
        logger.error(e)
        return True
    phone_number = result["sender_phone_number"]
    text = result["text"]
    status = "ok"
    try:
        feedback = get_feedback(phone_number)
        logger.debug(feedback)
    except CRMAPIError as e:
        logger.error(f"{e}\n{phone_number}\n{text}")
        return True
    if not feedback:
        logger.info(f"{phone_number} is trying to make feedback '{text}' secong time")
        return None
    data = change_feedback_data(feedback, status, text)
    try:
        send_put_request_to_crm(data)
    except CRMAPIError as e:
        logger.error(e)
    return True


def get_feedback(phone_number: str):
    url = f"{CRM_URL}/api/feedback/"
    headers = {"Authorization": f"Token {CRM_TOKEN}"}
    params = {
        "phone": phone_number, 
        "results[]": "message_send",
        "start_date": "2020-01-01",
        "end_date": "2040-01-01"
              }
    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        raise CRMAPIError("e")
    if response.status_code == 200:
        data = response.json()
        results = data.get("results")
        logger.info(f"Received feedbacks from CRM:{results}")
        if results:
            return results[0]
        else:
            return None
    raise CRMAPIError("Invalid response from CRM")


def change_feedback_data(feedback, status, text):
    
    data = {
        "id": feedback["id"],
        "order": feedback["order"]["id"],
        "result_id": status,
        "comment": text
    }
    logger.info(f"data for put request {data}")
    return data


def send_put_request_to_crm(data):
    feedback_id = data.get("id")
    url = f"{CRM_URL}/api/feedback/{feedback_id}/"
    headers = {"Authorization": f"Token {CRM_TOKEN}"}
    try:
        response = requests.put(
            url=url, headers=headers, data=data
        )
        logger.info(response)
    except ConnectionError as e:
        raise CRMAPIError("e")


def create_middle_grade_feedback(notification: Notification) -> None:
    try:
        result = parse_notification(notification)
    except GreenAPIError as e:
        logger.error(e)
        return True
    phone_number = result["sender_phone_number"]
    text = result["text"]
    status = "nok"
    try:
        feedback = get_feedback(phone_number)
    except CRMAPIError as e:
        logger.error(f"{e}\n{phone_number}\n{text}")
        return True
    if not feedback:
        logger.info(f"{phone_number} is trying to make feedback '{text}' secong time")
        return None
    data = change_feedback_data(feedback, status, text)
    try:
        send_put_request_to_crm(data)
    except CRMAPIError as e:
        logger.error(e)
    return True


def create_low_grade_feedback(notification: Notification) -> None:
    try:
        result = parse_notification(notification)
    except GreenAPIError as e:
        logger.error(e)
        return True
    phone_number = result["sender_phone_number"]
    text = result["text"]
    status = "critical"
    try:
        feedback = get_feedback(phone_number)
    except CRMAPIError as e:
        logger.error(f"{e}\n{phone_number}\n{text}")
        return True
    if not feedback:
        logger.info(f"{phone_number} is trying to make feedback '{text}' secong time")
        return None
    data = change_feedback_data(feedback, status, text)
    try:
        send_put_request_to_crm(data)
    except CRMAPIError as e:
        logger.error(e)
    return True