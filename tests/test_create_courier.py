# tests/test_create_courier.py

import allure
import pytest
from helpers import assert_response_status, assert_response_message
from page_objects.courier_api import CourierAPI
from response_messages import COURIER_CREATE_ERRORS

@allure.feature("Создание курьера")
class TestCourierAPI:

    @allure.title("Успешное создание курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self, new_courier_data):
        """Тест на успешное создание курьера"""
        courier_api = CourierAPI()  # Объект создается прямо в тесте

        with allure.step("Отправка запроса на создание нового курьера"):
            response = courier_api.create_courier(**new_courier_data)

        with allure.step("Проверка, что код ответа 201"):
            assert_response_status(response, 201, "Курьер не был создан")

        with allure.step("Проверка, что в теле ответа 'ok': true"):
            assert response.json().get("ok") is True, "Ответ не содержит 'ok': true"

    @allure.title("Создание двух одинаковых курьеров")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_duplicate_courier(self, new_courier_data):
        """Тест на создание двух курьеров с одинаковыми данными"""
        courier_api = CourierAPI()
        # Создаем первого курьера
        with allure.step("Создание первого курьера"):
            response = courier_api.create_courier(**new_courier_data)
            assert_response_status(response, 201)

        # Попытка создать второго курьера с тем же логином
        with allure.step("Попытка создания второго курьера с теми же данными"):
            response = courier_api.create_courier(**new_courier_data)

        with allure.step("Проверка кода ответа 409"):
            assert_response_status(response, 409)

        # Проверка сообщения об ошибке
        with allure.step("Проверка сообщения об ошибке"):
            assert_response_message(response, COURIER_CREATE_ERRORS["duplicate_login"])

    @allure.title("Создание курьера без обязательных полей")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["login", "password"])  # Убрали 'firstName'
    def test_create_courier_missing_fields(self, new_courier_data, missing_field):
        """Тест на создание курьера с отсутствующими обязательными полями"""
        courier_api = CourierAPI()

        # Убираем одно обязательное поле
        with allure.step(f"Отправка запроса с отсутствующим полем: {missing_field}"):
            incomplete_data = new_courier_data.copy()  # Создаем копию данных курьера
            incomplete_data.pop(missing_field)  # Удаляем отсутствующее поле

            # Отправляем запрос на создание курьера без обязательного поля
            response = courier_api.create_courier(
                login=incomplete_data.get('login'),
                password=incomplete_data.get('password')
            )

        with allure.step("Проверка кода ответа 400"):
            assert_response_status(response, 400)

        with allure.step("Проверка сообщения об ошибке"):
            assert_response_message(response, COURIER_CREATE_ERRORS["missing_data"])
