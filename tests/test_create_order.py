import allure
import pytest
from test_data import ORDER_COLORS  # Импорт данных о цветах

@allure.feature('Создание заказа')
@allure.story('Проверка создания заказа с разными параметрами цвета')
@pytest.mark.parametrize("color", ORDER_COLORS)
def test_create_order_with_different_colors(order_api, order_data, color):
    """Тест создания заказа с различными цветами: BLACK, GREY, оба или без цвета"""

    # Обновляем данные заказа с параметрами цвета
    order_data["color"] = color

    with allure.step(f"Отправка запроса на создание заказа с цветами: {color}"):
        response = order_api.create_order(order_data)

    with allure.step("Проверка, что запрос прошел успешно"):
        assert response.status_code == 201, f"Ожидался статус 201, получен: {response.status_code}"

    with allure.step("Проверка, что в ответе есть трек"):
        assert "track" in response.json(), "В ответе отсутствует поле 'track'"
