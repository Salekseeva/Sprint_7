# conftest.py

import pytest
import random
import string
from datetime import datetime, timedelta
from page_objects.courier_api import CourierAPI
from page_objects.order_api import OrderAPI

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

@pytest.fixture
def order_data():
    """Фикстура для генерации данных нового заказа"""
    return {
        "firstName": generate_random_string(8),  # строка из 8 случайных букв
        "lastName": generate_random_string(8),   # строка из 8 случайных букв
        "address": generate_random_address(),    # адрес в формате как в примере
        "metroStation": random.randint(1, 10),   # случайное число от 1 до 10
        "phone": generate_random_phone(),        # телефон с "+7 915" и 7 случайными цифрами
        "rentTime": random.randint(1, 7),        # случайное число от 1 до 7
        "deliveryDate": generate_future_date(3), # текущая дата + 3 дня
        "comment": generate_random_string(20)    # строка из 20 случайных букв/цифр/пробелов
    }

@pytest.fixture(scope='function')
def courier_api():
    """Фикстура для инициализации объекта CourierAPI"""
    return CourierAPI()

@pytest.fixture
def new_courier_data():
    """Фикстура для генерации данных нового курьера"""
    return {
        "login": generate_random_string(8),
        "password": generate_random_string(8),
        # Убираем поле firstName, так как оно не обязательно
    }

@pytest.fixture(scope='function')
def order_api():
    """Фикстура для инициализации объекта OrderAPI"""
    return OrderAPI()
