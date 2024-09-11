# tests/test_create_order.py

import allure
import pytest
from test_data import ORDER_COLORS  # Импорт данных о цветах
from page_objects.order_api import OrderAPI
from asserts import assert_response_status


#@allure.feature('Создание заказа')
class TestCreateOrderAPI:
    @allure.title('Проверка создания заказа с разными параметрами цвета')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("color", ORDER_COLORS)
    def test_create_order_with_different_colors(self, order_data, color):
        """Тест создания заказа с различными цветами: BLACK, GREY, оба или без цвета"""
        order_api = OrderAPI()

        # Обновляем данные заказа с параметрами цвета
        order_data["color"] = color

        with allure.step(f"Отправка запроса на создание заказа с цветами: {color}"):
            response = order_api.create_order(**order_data)

        with allure.step("Проверка, что запрос прошел успешно"):
            assert_response_status(response, 201)

        with allure.step("Проверка, что в ответе есть трек"):
            assert "track" in response.json(), "В ответе отсутствует поле 'track'"
