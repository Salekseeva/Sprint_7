# helpers.py

import random
import string
from datetime import datetime, timedelta

def generate_random_string(length=8):
    """Генерация случайной строки из букв"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_address():
    """Генерация адреса: 20 случайных символов, затем запятая, пробел и от 1 до 3 случайных чисел"""
    address_part = ''.join(random.choice(string.ascii_letters) for _ in range(20))
    number_part = ''.join(random.choice(string.digits) for _ in range(random.randint(1, 3)))
    return f"{address_part}, {number_part}"

def generate_random_phone():
    """Генерация номера телефона: +7 915 и 7 случайных чисел"""
    return "+7 915 " + ''.join(random.choice(string.digits) for _ in range(7))

def generate_future_date(days_in_future=3):
    """Генерация даты, текущая дата + несколько дней"""
    return (datetime.now() + timedelta(days=days_in_future)).strftime('%Y-%m-%d')

def assert_response_status(response, expected_status, message=""):
    assert response.status_code == expected_status, f"{message}. Ожидался код {expected_status}, получен {response.status_code}"

def assert_response_message(response, expected_message):
    assert expected_message in response.json().get("message"), \
        f"Ожидалось сообщение '{expected_message}', получено '{response.json().get('message')}'"
