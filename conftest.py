# conftest.py

import pytest
import random
from page_objects.courier_api import CourierAPI
from page_objects.order_api import OrderAPI
from helpers import generate_random_string, generate_random_address, generate_random_phone, generate_future_date

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

@pytest.fixture
def new_courier_data():
    """Фикстура для генерации данных нового курьера"""
    return {
        "login": generate_random_string(8),
        "password": generate_random_string(8),
        # Убираем поле firstName, так как оно не обязательно
    }


@pytest.fixture
def created_courier(new_courier_data):
    """Предусловие: создание курьера перед тестом"""
    courier_api = CourierAPI()

    # Удаляем курьера, если он существует
    courier_id = courier_api.get_courier_id(new_courier_data["login"])
    if courier_id:
        courier_api.delete_courier(courier_id)

    # Создаем курьера
    response = courier_api.create_courier(**new_courier_data)

    # Возвращаем response и данные курьера для использования в тестах
    return {
        "response": response,
        "courier_data": new_courier_data
    }
