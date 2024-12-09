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


class FeedbackNotFoundError(Exception):
    """Error when feedback not found"""


class CRMConnectionError(Exception):
    """Error when connecting to CRM"""

class NotificationDecodeError(Exception):
    """Error when decoding Green-API object"""


def parse_notification(notification: Notification):
    sender = notification.get_sender()
    if sender:
        sender_phone_number = "+" + re.sub("@c.us", "", sender)
    else:
        raise GreenAPIError("Sender not found")
    message_text = notification.get_message_text()
    return {"sender_phone_number": sender_phone_number, "text": message_text}


def create_five_points_feedback(notification: Notification) -> None:
    logger.info("creating high grade feedback")
    try:
        result = parse_notification(notification)
    except GreenAPIError as e:
        logger.debug(e)
        raise NotificationDecodeError(e)
    phone_number = result["sender_phone_number"]
    text = result["text"]
    status = "ok"
    try:
        feedback = get_feedback(phone_number)
        logger.debug(feedback)
    except CRMAPIError as e:
        logger.debug(f"{e}\n{phone_number}\n{text}")
        raise CRMConnectionError(e)
    if not feedback:
        raise FeedbackNotFoundError(f"{phone_number} is trying to make feedback '{text}' secong time")
    data = change_feedback_data(feedback, status, text)
    try:
        send_put_request_to_crm(data)
    except CRMAPIError as e:
        logger.debug(e)
        raise CRMConnectionError(e)
    return True


def get_feedback(phone_number: str):
    url = f"{CRM_URL}/api/feedback/"
    headers = {"Authorization": f"Token {CRM_TOKEN}"}
    #В апи 
    params = {"phone": phone_number}
    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        raise CRMAPIError("e")
    if response.status_code == 200:
        data = response.json()
        results = data.get("results")
        #logger.info(f"Received feedbacks from CRM:{results}")
        if results:
            message_send_results =  list(filter(lambda x: x.get("result", {}).get("id") == "message_send", results))
        else:
            return None
        if not message_send_results:
            return None
        message_send_results.sort(key=lambda x: x.get("order", {}).get("order_date"), reverse=True)
        return message_send_results[0]
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
    logger.info("creating middle grade request")
    try:
        result = parse_notification(notification)
    except GreenAPIError as e:
        logger.debug(f"raising NotificationDecodeError {e}")
        raise NotificationDecodeError(e)
    phone_number = result["sender_phone_number"]
    text = result["text"]
    status = "nok"
    try:
        feedback = get_feedback(phone_number)
        logger.info(feedback)
    except CRMAPIError as e:
        logger.debug(f"raising CRMConnectionError {e}")
        raise CRMConnectionError(e)
    if not feedback:
        logger.debug("raising FeedbackNotFoundError")
        raise FeedbackNotFoundError(f"{phone_number} is trying to make feedback '{text}' secong time")
    data = change_feedback_data(feedback, status, text)
    try:
        send_put_request_to_crm(data)
    except CRMAPIError as e:
        logger.debug(f"Raising CRMConnectionError {e}")
        raise CRMConnectionError(e)
    return True


def create_low_grade_feedback(notification: Notification) -> None:
    logger.info("creating low grade feedback")
    try:
        result = parse_notification(notification)
    except GreenAPIError as e:
        logger.debug(e)
        raise NotificationDecodeError(e)
    phone_number = result["sender_phone_number"]
    text = result["text"]
    status = "critical"
    try:
        feedback = get_feedback(phone_number)
        logger.debug(feedback)
    except CRMAPIError as e:
        logger.debug(f"{e}\n{phone_number}\n{text}")
        raise CRMConnectionError(e)
    if not feedback:
        raise FeedbackNotFoundError(f"{phone_number} is trying to make feedback '{text}' secong time")
    data = change_feedback_data(feedback, status, text)
    try:
        send_put_request_to_crm(data)
    except CRMAPIError as e:
        logger.debug(e)
        raise CRMConnectionError(e)
    return True