## page_objects/order_api.py

import requests
from config import ORDER_API_URL

class OrderAPI:
    BASE_URL = ORDER_API_URL

    def get_orders(self, courier_id=None):
        """Получение списка заказов с возможностью фильтрации по courierId"""
        params = {}
        if courier_id is not None:
            params["courierId"] = courier_id
        return requests.get(self.BASE_URL, params=params)

    def create_order(self, firstName, lastName, address, metroStation, phone, rentTime, deliveryDate, comment, color=None):
        """Создание заказа с указанными данными"""
        data = {
        "firstName": firstName,
        "lastName": lastName,
        "address": address,
        "metroStation": metroStation,
        "phone": phone,
        "rentTime": rentTime,
        "deliveryDate": deliveryDate,
        "comment": comment
        }
        if color:
            data["color"] = color

        return requests.post(self.BASE_URL, json=data)

    # Метод для получения заказа по трек-номеру
    def get_order_by_track(self, track):
        """Получение заказа по трек-номеру"""
        params = {"t": track}
        return requests.get(f"{self.BASE_URL}/track", params=params)
