# response_messages.py

from test_data import INVALID_COURIER_ID

COURIER_LOGIN_ERRORS = {
    "missing_data": "Недостаточно данных для входа",
    "courier_not_found": "Курьер с идентификатором {id} не найден",
    "account_not_found": "Учетная запись не найдена"
}

COURIER_CREATE_ERRORS = {
    "missing_data": "Недостаточно данных для создания учетной записи",
    "duplicate_login": "Этот логин уже используется"
}

ORDER_ERRORS = {
    "order_not_found": "Заказ с трек-номером {track} не найден",
    "invalid_courier_id": "Курьер с идентификатором {id} не найден"
}
