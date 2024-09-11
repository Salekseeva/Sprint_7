def assert_response_status(response, expected_status, message=""):
    """Проверка статуса ответа"""
    assert response.status_code == expected_status, \
        f"{message}. Ожидался код {expected_status}, получен {response.status_code}"

def assert_response_message(response, expected_message):
    """Проверка сообщения в ответе"""
    actual_message = response.json().get("message")
    assert expected_message in actual_message, \
        f"Ожидалось сообщение '{expected_message}', получено '{response.json().get('message')}'"
