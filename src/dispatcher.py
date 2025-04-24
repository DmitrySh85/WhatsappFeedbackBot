from whatsapp_chatbot_python import GreenAPIBot, Notification, filters
from states.states import States
from settings import ID_INSTANCE, API_TOKEN_INSTANCE
from services.handlers_services import(
    create_five_points_feedback,
    create_middle_grade_feedback,
    create_low_grade_feedback,
    create_high_grade_feedback,
    create_unrecognized_feedback,
    parse_notification,
    NotificationDecodeError,
    CRMConnectionError,
    FeedbackNotFoundError,
    GreenAPIError
)
from static_text.static_text import (
    FIVE_POINTS_GRADE_TEXT,
    ANOTHER_GRADES_TEXT,
    GOODBYE_MESSAGE_TEXT,
    SECOND_TIME_FEEDBACK_ATTEMPT
)
from bot_logger import init_logger
from yandex.manager import YandexAPIManager
import json


logger = init_logger(__name__)


bot = GreenAPIBot(
    ID_INSTANCE, API_TOKEN_INSTANCE
)


@bot.router.message(
        type_message=filters.TEXT_TYPES,
        state=None,
        text_message=[
            '0', 'Ноль', 'ноль', 'Полный ноль', 'Нуль', 'нуль',
            '1', 'Один', 'один', 'Один балл', 'один балл', '1 балл', "1!", "1-", "1+", "1(один)",
            '2', 'Два', 'два', 'Два балла', 'два балла', '2 балла', "2!", "двойка", "2-", "2(двойка)", "неуд"
        ])
def low_grade_message_handler(notification: Notification):
    logger.info(notification.event)
    logger.info(notification.state_manager.get_state(notification.sender))
    notification.state_manager.update_state(
        notification.sender,
        States.LOW_GRADE
    )
    notification.answer(ANOTHER_GRADES_TEXT)


@bot.router.message(type_message=filters.TEXT_TYPES,
                    state=None,
                    text_message=[
                        '3', 'Три', 'три', 'Три балла', 'три балла', '3 балла', "3!", "3-", "3+"
                        ]
                        )
def middle_grade_message_handler(notification: Notification):
    logger.info(notification.state_manager.get_state(notification.sender))
    notification.state_manager.update_state(
        notification.sender,
        States.MIDDLE_GRADE
    )
    notification.answer(ANOTHER_GRADES_TEXT)


@bot.router.message(type_message=filters.TEXT_TYPES,
                    state=None,
                    text_message=[
                        '4', 'Четыре', 'четыре', 'Четыре балла', 'четыре балла', '4 балла', "4!", "4-", "4+"
                                   ])
def hight_grade_message_handler(notification: Notification):
    logger.info(notification.state_manager.get_state(notification.sender))
    notification.state_manager.update_state(
        notification.sender,
        States.HIGH_GRADE
    )
    notification.answer(ANOTHER_GRADES_TEXT)


@bot.router.message(
        type_message=filters.TEXT_TYPES,
        state=States.LOW_GRADE
        )
def low_grades_explain_handler(notification: Notification):
    logger.info(notification.event)
    logger.info("process low grade")
    logger.info(notification.state_manager.get_state(notification.sender))
    try:
        create_low_grade_feedback(notification)
    except Exception as e:
        logger.debug(e)
        notification.state_manager.delete_state(
            notification.sender
        )
        return
    notification.answer(GOODBYE_MESSAGE_TEXT)
    notification.state_manager.delete_state(
        notification.sender
    )


@bot.router.message(
        type_message=filters.TEXT_TYPES,
        state=States.MIDDLE_GRADE
        )
def middle_grades_explain_handler(notification: Notification):
    logger.info(notification.event)
    logger.info("process middle grade")
    logger.info(notification.state_manager.get_state(notification.sender))
    try:
        create_middle_grade_feedback(notification)
    except Exception as e:
        logger.debug(e)
        notification.state_manager.delete_state(
            notification.sender
        )
        return
    notification.answer(GOODBYE_MESSAGE_TEXT)
    notification.state_manager.delete_state(
        notification.sender
    )


@bot.router.message(
        type_message=filters.TEXT_TYPES,
        state=States.HIGH_GRADE
        )
def high_grades_explain_handler(notification: Notification):
    logger.info(notification.event)
    logger.info("process high grade")
    logger.info(notification.state_manager.get_state(notification.sender))
    try:
        create_high_grade_feedback(notification)
    except Exception as e:
        logger.debug(e)
        notification.state_manager.delete_state(
            notification.sender
        )
        return
    notification.answer(GOODBYE_MESSAGE_TEXT)
    notification.state_manager.delete_state(
        notification.sender
    )



@bot.router.message(type_message=filters.TEXT_TYPES,
                    state=None,
                    text_message=[
                        "5", 
                        "5 баллов", 
                        "Пять", 
                        "пять", 
                        "Пять баллов",
                        "Пять балов",
                        "пять балов"
                        "5 (пять)",
                        "5(пять) баллов",
                        "5!",
                        "5+",
                        "5-",
                        "отлично",
                        "Отлично"
                        ])
def process_five_points_grade(notification: Notification): 
    logger.info(notification.event)
    logger.info("process high grade")
    logger.info(notification.state_manager.get_state(notification.sender))
    try:
        create_five_points_feedback(notification)
    except Exception as e:
        logger.debug(e)
    


@bot.router.message()
def process_another_feedback(notification: Notification):
    logger.info(notification.state_manager.get_state(notification.sender))
    logger.info(notification.event)
    try:
        result = parse_notification(notification)
    except GreenAPIError as e:
        logger.debug(e)
        return
    if not result:
        return
    message_text = result.get("text")
    api_manager = YandexAPIManager()
    try:
        ai_response = api_manager.send_recognition_request(message_text)
        response_data = f"Оценка АИ: {ai_response.get('grade', '')}\nКомментарий АИ: {ai_response.get('description', '')}"
    except Exception as e:
        response_data = e
    try:
        create_unrecognized_feedback(notification, response_data)
    except (NotificationDecodeError, CRMConnectionError, FeedbackNotFoundError) as e:
        logger.debug(e)