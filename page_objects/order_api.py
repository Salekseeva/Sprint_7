## page_objects/order_api.py

import requests

class OrderAPI:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

    def get_orders(self, courier_id=None):
        """Получение списка заказов с возможностью фильтрации по courierId"""
        params = {}
        if courier_id:
            params["courierId"] = courier_id
        return requests.get(self.BASE_URL, params=params)

    def create_order(self, order_data):
        """Создание заказа с указанными данными"""
        response = requests.post(self.BASE_URL, json=order_data)
        return response
