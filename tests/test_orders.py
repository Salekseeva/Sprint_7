# tests/test_orders.py

import allure
import pytest
from test_data import INVALID_COURIER_ID  # Импорт тестовых данных
from asserts import assert_response_status
from page_objects.order_api import OrderAPI
from response_messages import ORDER_ERRORS


@allure.feature("Заказы")
class TestOrderAPI:

    # Тест на успешное получение списка заказов
    @allure.title("Получение списка заказов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка, что при успешном запросе возвращается список заказов")
    def test_get_orders_without_courier_id(self):
        """Тест на успешное получение списка заказов без указания courierId"""
        order_api = OrderAPI()

        with allure.step("Отправка GET-запроса на получение списка заказов без courierId"):
            response = order_api.get_orders()

        with allure.step("Проверка, что статус код равен 200"):
#            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            assert_response_status(response, 200, "Список заказов не получен.")

        with allure.step("Проверка, что в теле ответа присутствует ключ 'orders'"):
            assert "orders" in response.json(), "Ответ не содержит ключа 'orders'"

        with allure.step("Проверка, что список заказов не пустой"):
            assert len(response.json()["orders"]) > 0, "Список заказов пуст"

    @allure.title("Создание заказа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_success(self, order_data):
        """Тест на успешное создание заказа"""
        order_api = OrderAPI()  # Объект создается прямо в тесте

        with allure.step("Отправка POST-запроса на создание нового заказа"):
            response = order_api.create_order(**order_data)

        with allure.step("Проверка, что статус код равен 201"):
            assert_response_status(response, 201)

        with allure.step("Проверка, что в ответе содержится 'track'"):
            assert "track" in response.json(), "Ответ должен содержать поле 'track'"

    @allure.title("Получение заказа по трек-номеру")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_order_by_track(self, order_data):
        """Тест на получение заказа по трек-номеру"""
        order_api = OrderAPI()  # Объект создается прямо в тесте

        with allure.step("Создание нового заказа"):
            response = order_api.create_order(**order_data)
            assert_response_status(response, 201)
            track = response.json().get("track")

        with allure.step(f"Получение заказа по трек-номеру: {track}"):
            response = order_api.get_order_by_track(track)
            assert_response_status(response, 200)

        with allure.step("Проверка, что в ответе есть информация о заказе"):
            assert "order" in response.json(), "Ответ должен содержать информацию о заказе"

    # Тест на ошибку при несуществующем courierId
    @allure.title("Получение списка заказов с несуществующим courierId")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка, что при передаче несуществующего courierId возвращается ошибка 404")
    def test_get_orders_with_invalid_courier_id(self):
        order_api = OrderAPI()

        with allure.step(f"Отправка GET-запроса на получение списка заказов с несуществующим courierId={INVALID_COURIER_ID}"):
            response = order_api.get_orders(courier_id=INVALID_COURIER_ID)

        with allure.step("Проверка, что статус код равен 404"):
            assert_response_status(response, 404)

        with allure.step("Проверка, что в теле ответа присутствует сообщение об ошибке"):
            assert "message" in response.json(), "Ответ не содержит ключа 'message'"
            assert response.json()["message"] == ORDER_ERRORS["invalid_courier_id"].format(id=INVALID_COURIER_ID), \
                "Сообщение об ошибке не соответствует ожидаемому"
