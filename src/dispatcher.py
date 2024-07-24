from whatsapp_chatbot_python import GreenAPIBot, Notification, filters
from states.states import States
from settings import ID_INSTANCE, API_TOKEN_INSTANCE
from services.handlers_services import(
    create_five_points_feedback,
    create_middle_grade_feedback,
    create_low_grade_feedback
)
from static_text.static_text import (
    UNKNOWN_TYPE_MESSAGE_TEXT,
    FIVE_POINTS_GRADE_TEXT,
    ANOTHER_GRADES_TEXT,
    GOODBYE_MESSAGE_TEXT,
    SECOND_TIME_FEEDBACK_ATTEMPT
)
from bot_logger import init_logger


logger = init_logger(__name__)


bot = GreenAPIBot(
    ID_INSTANCE, API_TOKEN_INSTANCE
)


@bot.router.message(type_message=filters.TEXT_TYPES,
                    state=None,
                    text_message=['1', '2'])
def low_grade_message_handler(notification: Notification):
    notification.state_manager.update_state(
        notification.sender,
        States.LOW_GRADE
    )
    notification.answer(ANOTHER_GRADES_TEXT)


@bot.router.message(type_message=filters.TEXT_TYPES,
                    state=None,
                    text_message=['3', '4'])
def middle_grade_message_handler(notification: Notification):
    notification.state_manager.update_state(
        notification.sender,
        States.MIDDLE_GRADE
    )
    notification.answer(ANOTHER_GRADES_TEXT)



@bot.router.message(type_message=filters.TEXT_TYPES,
                    state=States.LOW_GRADE)
def low_grades_explain_handler(notification: Notification):
    created = create_low_grade_feedback(notification)
    try:
        logger.debug(notification.event, created)
    except TypeError:
        logger.debug("Failed to log lotification")
    if not created:
        notification.answer(SECOND_TIME_FEEDBACK_ATTEMPT)
        notification.state_manager.delete_state(
            notification.sender
        )
        return
    notification.answer(GOODBYE_MESSAGE_TEXT)
    notification.state_manager.delete_state(
        notification.sender
    )


@bot.router.message(type_message=filters.TEXT_TYPES,
                    state=States.MIDDLE_GRADE)
def middle_grades_explain_handler(notification: Notification):
    created = create_middle_grade_feedback(notification)
    try:
        logger.debug(notification.event, created)
    except TypeError:
        logger.debug("Failed to log lotification")
    if not created:
        notification.answer(SECOND_TIME_FEEDBACK_ATTEMPT)
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
                    text_message=["5", "5 баллов", "Пять", "пять"])
def process_five_points_grade(notification: Notification): 
    created = create_five_points_feedback(notification)
    try:
        logger.debug(notification.event, created)
    except TypeError:
        logger.debug("Failed to log lotification")
    if not created:
        return notification.answer(SECOND_TIME_FEEDBACK_ATTEMPT)
    notification.answer(FIVE_POINTS_GRADE_TEXT)


@bot.router.message()
def process_another_feedback(notification: Notification):
    notification.answer(UNKNOWN_TYPE_MESSAGE_TEXT[0])
    notification.answer(UNKNOWN_TYPE_MESSAGE_TEXT[1])
