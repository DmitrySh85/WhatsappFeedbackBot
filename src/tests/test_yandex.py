import pytest
from yandex.manager import YandexAPIManager


def test_yandex_success():
    manager = YandexAPIManager()
    text = 'написал в вотсапе. загорелось лопасть вентилятора радиатора. не доволен'
    result = manager.send_recognition_request(text)
    assert result.get("description") is not None


def test_yandex_five_points():
    manager = YandexAPIManager()
    text = '5'
    result = manager.send_recognition_request(text)
    assert result.get("grade") == '5'
    assert result.get("description") is not None


def test_yandex_four_points():
    manager = YandexAPIManager()
    text = 'Четыре балла'
    result = manager.send_recognition_request(text)
    assert result.get("grade") == '4'
    assert result.get("description") is not None

def test_yandex_thrash_message():
    manager = YandexAPIManager()
    text = 'привет'
    result = manager.send_recognition_request(text)
    assert result.get("description") == 'Сообщение не содержало оценки качества работы сервиса'