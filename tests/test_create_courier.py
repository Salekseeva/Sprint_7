# tests/test_create_courier.py

import allure
import pytest


@allure.feature("Создание курьера")
class TestCourierAPI:

    @allure.story("Успешное создание курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self, courier_api, new_courier_data):
        """Тест на успешное создание курьера"""
        with allure.step("Отправка запроса на создание нового курьера"):
            response = courier_api.create_courier(**new_courier_data)

        with allure.step("Проверка, что код ответа 201"):
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"

        with allure.step("Проверка, что в теле ответа 'ok': true"):
            assert response.json().get("ok") is True, "Ответ не содержит 'ok': true"

    @allure.story("Создание двух одинаковых курьеров")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_duplicate_courier(self, courier_api, new_courier_data):
        """Тест на создание двух курьеров с одинаковыми данными"""
        # Создаем первого курьера
        with allure.step("Создание первого курьера"):
            response = courier_api.create_courier(**new_courier_data)
            assert response.status_code == 201, f"Первый курьер не был создан. Код ответа: {response.status_code}"

        # Попытка создать второго курьера с тем же логином
        with allure.step("Попытка создания второго курьера с теми же данными"):
            response = courier_api.create_courier(**new_courier_data)

        with allure.step("Проверка кода ответа 409"):
            assert response.status_code == 409, f"Ожидался код 409, получен {response.status_code}"

        # Проверка сообщения об ошибке
        with allure.step("Проверка сообщения об ошибке"):
            assert "Этот логин уже используется" in response.json().get("message"), \
                f"Ожидалось сообщение 'Этот логин уже используется', получено {response.json().get('message')}"

    @allure.story("Создание курьера без обязательных полей")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["login", "password"])  # Убрали 'firstName'
    def test_create_courier_missing_fields(self, courier_api, new_courier_data, missing_field):
        """Тест на создание курьера с отсутствующими обязательными полями"""
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
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json().get("message") == "Недостаточно данных для создания учетной записи", \
                f"Ожидалось сообщение 'Недостаточно данных для создания учетной записи', получено {response.json().get('message')}"

    @allure.story("Создание курьера с уже существующим логином")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_existing_login(self, courier_api, new_courier_data):
        """Тест на создание курьера с уже существующим логином"""
        # Создаем курьера с уникальными данными
        with allure.step("Создание курьера с уникальным логином"):
            response = courier_api.create_courier(**new_courier_data)
            assert response.status_code == 201, f"Первый курьер не был создан. Код ответа: {response.status_code}"

        # Пытаемся создать курьера с тем же логином
        with allure.step("Попытка создания курьера с уже существующим логином"):
            response = courier_api.create_courier(**new_courier_data)
            assert response.status_code == 409, f"Ожидался код 409, получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert "Этот логин уже используется" in response.json().get("message"), \
                f"Ожидалось сообщение 'Этот логин уже используется', получено {response.json().get('message')}"
