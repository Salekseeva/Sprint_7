# tests/courier_login.py

import allure
import requests
import pytest
from page_objects.courier_api import CourierAPI

@allure.feature("Авторизация курьера")
class TestCourierLoginAPI:

    @allure.story("Успешная авторизация курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_courier_success(self, courier_api, new_courier_data):
        """Тест на успешную авторизацию курьера"""
        # Уникальные данные для логина
        login_data = new_courier_data

        # Удаляем курьера, если он существует
        courier_id = courier_api.get_courier_id(login_data["login"])
        if courier_id:
            courier_api.delete_courier(courier_id)

        # Создаем курьера
        response = courier_api.create_courier(**login_data)
        assert response.status_code == 201, f"Курьер не был создан. Код ответа: {response.status_code}"

        # Авторизация курьера с таймаутом
        with allure.step("Отправка запроса на авторизацию"):
            response = requests.post(f"{CourierAPI.BASE_URL}/login", json=login_data, timeout=10)

        with allure.step("Проверка кода ответа 200"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        with allure.step("Проверка, что в теле ответа есть поле 'id'"):
            assert "id" in response.json(), "Ответ не содержит поле 'id'"

    @allure.story("Ошибка при отсутствии обязательных полей")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_fields(self, courier_api, missing_field):
        """Тест на авторизацию с отсутствующим обязательным полем"""
        login_data = {
            "login": "test_login",
            "password": "test_password"
        }

        # Заменяем отсутствующее поле на пустую строку
        login_data[missing_field] = ""  # Оставляем поле, но делаем его пустым

        with allure.step(f"Отправка запроса с пустым полем: {missing_field}"):
            response = requests.post(f"{CourierAPI.BASE_URL}/login", json=login_data, timeout=10)

        with allure.step("Проверка кода ответа 400"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json().get("message") == "Недостаточно данных для входа", \
                f"Ожидалось сообщение 'Недостаточно данных для входа', получено {response.json().get('message')}"
