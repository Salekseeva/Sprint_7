# tests/test_orders.py

import allure
import pytest
from test_data import INVALID_COURIER_ID  # Импорт тестовых данных

# Тест на успешное получение списка заказов
@allure.title("Получение списка заказов без указания courierId")
@allure.description("Проверка, что при успешном запросе возвращается список заказов")
def test_get_orders_without_courier_id(order_api):
    with allure.step("Отправка GET-запроса на получение списка заказов без courierId"):
        response = order_api.get_orders()

    with allure.step("Проверка, что статус код равен 200"):
        assert response.status_code == 200, "Ожидаемый статус код 200, но получен другой"

    with allure.step("Проверка, что в теле ответа присутствует ключ 'orders'"):
        assert "orders" in response.json(), "Ответ не содержит ключа 'orders'"

    with allure.step("Проверка, что список заказов не пустой"):
        assert len(response.json()["orders"]) > 0, "Список заказов пуст"

# Тест на ошибку при несуществующем courierId
@allure.title("Получение списка заказов с несуществующим courierId")
@allure.description("Проверка, что при передаче несуществующего courierId возвращается ошибка 404")
def test_get_orders_with_invalid_courier_id(order_api):
    with allure.step(f"Отправка GET-запроса на получение списка заказов с несуществующим courierId={INVALID_COURIER_ID}"):
        response = order_api.get_orders(courier_id=INVALID_COURIER_ID)

    with allure.step("Проверка, что статус код равен 404"):
        assert response.status_code == 404, "Ожидаемый статус код 404, но получен другой"

    with allure.step("Проверка, что в теле ответа присутствует сообщение об ошибке"):
        assert "message" in response.json(), "Ответ не содержит ключа 'message'"
        assert response.json()["message"] == f"Курьер с идентификатором {INVALID_COURIER_ID} не найден", \
            "Сообщение об ошибке не соответствует ожидаемому"
