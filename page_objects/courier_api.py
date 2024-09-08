# page_objects/courier_api.py

import requests

class CourierAPI:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

    def create_courier(self, login, password, firstName=None):
        """Создание курьера с указанными параметрами"""
        payload = {
            "login": login,
            "password": password,
        }
        if firstName:
            payload["firstName"] = firstName
        return requests.post(self.BASE_URL, json=payload)

    def delete_courier(self, courier_id):
        """Удаление курьера по его ID"""
        return requests.delete(f"{self.BASE_URL}/{courier_id}")

    def get_courier_id(self, login):
        """Получение ID курьера по логину"""
        response = requests.get(f"{self.BASE_URL}?login={login}")
        if response.status_code == 200 and "id" in response.json():
            return response.json()["id"]
        return None
