# tests/test_courier_login.py

import allure
import requests
import pytest
from page_objects.courier_api import CourierAPI
from helpers import assert_response_status, assert_response_message, generate_random_string
from test_data import COURIER_LOGIN_DATA
from response_messages import COURIER_LOGIN_ERRORS


@allure.feature("Авторизация курьера")
class TestCourierLoginAPI:

    @allure.title("Успешная авторизация курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_courier_success(self, created_courier):
        """Тест на успешную авторизацию курьера"""

        # Уникальные данные для логина
        login_data = created_courier

        # Авторизация курьера с таймаутом
        with allure.step("Отправка запроса на авторизацию"):
            response = requests.post(f"{CourierAPI.BASE_URL}/login", json=login_data, timeout=10)

        with allure.step("Проверка кода ответа 200"):
            assert_response_status(response, 200, "Курьер не был авотризован")

        with allure.step("Проверка, что в теле ответа есть поле 'id'"):
            assert "id" in response.json(), "Ответ не содержит поле 'id'"

    @allure.title("Ошибка при отсутствии обязательных полей")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_fields(self, missing_field):
        """Тест на авторизацию с отсутствующим обязательным полем"""

        login_data = COURIER_LOGIN_DATA.copy()

        login_data[missing_field] = ""  # Оставляем поле, но делаем его пустым

        with allure.step(f"Отправка запроса с пустым полем: {missing_field}"):
            response = requests.post(f"{CourierAPI.BASE_URL}/login", json=login_data, timeout=10)

        with allure.step("Проверка кода ответа 400"):
            assert_response_status(response, 400, "Недостаточно данных.")

        with allure.step("Проверка сообщения об ошибке"):
            assert_response_message(response, COURIER_LOGIN_ERRORS["missing_data"])

    @allure.title("Ошибка при авторизации с несуществующей парой логин-пароль")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_invalid_credentials(self):
        """Тест на авторизацию с несуществующими логином и паролем"""

        # Генерируем случайные логин и пароль, которые точно не существуют
        invalid_login_data = {
            "login": generate_random_string(10),  # Генерация случайного логина
            "password": generate_random_string(10)  # Генерация случайного пароля
        }

        with allure.step("Отправка запроса с несуществующей парой логин-пароль"):
            response = requests.post(f"{CourierAPI.BASE_URL}/login", json=invalid_login_data, timeout=10)

        with allure.step("Проверка кода ответа 404"):
            assert_response_status(response, 404, "Курьер с такими данными не найден.")

        with allure.step("Проверка сообщения об ошибке"):
            assert_response_message(response, COURIER_LOGIN_ERRORS["account_not_found"])