from bot_logger import init_logger

from deepseek.manager import DeepseekAPIManager


logger = init_logger(__name__)


def test_deepseek_success():
    manager = DeepseekAPIManager()
    text = 'написал в вотсапе. загорелось лопасть вентилятора радиатора. не доволен'
    result = manager.send_recognition_request(text)
    logger.info(result)
    assert result.get("description") is not None


def test_deepseek_five_points():
    manager = DeepseekAPIManager()
    text = '5'
    result = manager.send_recognition_request(text)
    assert result.get("grade") == '5'
    logger.info(result)
    assert result.get("description") is not None


def test_deepseek_four_points():
    manager = DeepseekAPIManager()
    text = 'Четыре балла'
    result = manager.send_recognition_request(text)
    assert result.get("grade") == '4'
    logger.info(result)
    assert result.get("description") is not None

def test_deepseek_thrash_message():
    manager = DeepseekAPIManager()
    text = 'привет'
    result = manager.send_recognition_request(text)
    logger.info(result)
    assert result.get("description") == 'Сообщение не содержало оценки качества работы сервиса'


def test_deepseek_explicit_five_with_text():
    manager = DeepseekAPIManager()
    text = 'Оценка 5! Очень доволен работой мастеров, всё сделали быстро и качественно'
    result = manager.send_recognition_request(text)
    assert result.get("grade") == '5'
    assert result.get("description") is not None
    logger.info(f"Explicit five: {result}")

def test_deepseek_one_point_with_complaint():
    manager = DeepseekAPIManager()
    text = 'Ставлю 1 балл. Ждал ремонт 3 часа, машину сделали плохо, пришлось переделывать'
    result = manager.send_recognition_request(text)
    assert result.get("grade") == '1'
    logger.info(f"One point with complaint: {result}")

def test_deepseek_three_points_emoji():
    manager = DeepseekAPIManager()
    text = 'Вот моя оценка: ⭐⭐⭐ из 5. Всё нормально, но есть небольшие недочёты'
    result = manager.send_recognition_request(text)
    assert result.get("grade") == '3'
    logger.info(f"Three points emoji: {result}")

def test_deepseek_text_based_rating():
    manager = DeepseekAPIManager()
    text = 'Работой автосервиса очень доволен, отличное обслуживание на пять с плюсом!'
    result = manager.send_recognition_request(text)
    assert result.get("grade") == '5'
    logger.info(f"Text-based rating: {result}")

def test_deepseek_neutral_thankyou():
    manager = DeepseekAPIManager()
    text = 'Спасибо за помощь! Буду рекомендовать ваш сервис друзьям'
    result = manager.send_recognition_request(text)
    assert "description" in result
    assert "grade" not in result
    assert "не содержало" in result.get("description", "").lower()
    logger.info(f"Neutral thankyou: {result}")

def test_deepseek_question_no_rating():
    manager = DeepseekAPIManager()
    text = 'Во сколько у вас открывается сервис в субботу?'
    result = manager.send_recognition_request(text)
    assert "description" in result
    assert "grade" not in result
    logger.info(f"Question no rating: {result}")

def test_deepseek_mixed_message():
    manager = DeepseekAPIManager()
    text = 'Привет! Хочу сказать, что в целом неплохо, но можно лучше. 4 балла'
    result = manager.send_recognition_request(text)
    assert "description" in result
    if "grade" in result:
        assert result["grade"] in ['1', '2', '3', '4', '5']
    logger.info(f"Mixed message: {result}")

def test_deepseek_negative_no_explicit_rating():
    manager = DeepseekAPIManager()
    text = 'Ужасный сервис, никогда больше не приеду. Деньги на ветер'
    result = manager.send_recognition_request(text)
    logger.info(f"Negative no explicit rating: {result}")

def test_deepseek_rating_in_middle():
    manager = DeepseekAPIManager()
    text = 'Приехал на ТО, обслужили нормально, ставлю 4 балла из 5, но цены высоковаты'
    result = manager.send_recognition_request(text)
    assert result.get("grade") == '4'
    logger.info(f"Rating in middle: {result}")

def test_deepseek_multiple_ratings():
    manager = DeepseekAPIManager()
    text = 'По качеству - 5, по скорости - 3, по цене - 2. В среднем 4 балла'
    result = manager.send_recognition_request(text)
    assert result.get("grade") in ['3', '4', '5']
    logger.info(f"Multiple ratings: {result}")