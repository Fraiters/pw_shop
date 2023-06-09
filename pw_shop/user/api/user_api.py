import traceback

from flask import Flask, jsonify
from pw_shop.user.user_db import UserDb
from server_utils.http_exception import BadRequest
from server_utils.request_data import get_request_data
from server_utils.url.url_constructor import UrlConstructor


app = Flask(__name__)
url = UrlConstructor().construct()  # "http://127.0.0.1:5000"


@app.route('/auth_user', methods=['POST'])
def auth_user():
    """АПИ для авторизации пользователя"""
    # получение данных запроса (логин, пароль)
    request_data = get_request_data()

    if not isinstance(request_data, dict):
        msg = "Неверный формат (ожидался словарь)"
        raise BadRequest(msg)

    login = request_data.get("login")
    password = request_data.get("password")

    if login is None:
        msg = "Данные логина неизвестны"
        raise BadRequest(msg)

    if password is None:
        msg = "Данные пароля неизвестны"
        raise BadRequest(msg)

    user_db = UserDb()
    response = user_db.auth_user(request_data=request_data)

    return jsonify(response)


@app.route('/registration_user', methods=['POST'])
def registration_user():
    """АПИ для авторизации пользователя"""
    # получение данных запроса (логин, пароль)
    request_data = get_request_data()

    if not isinstance(request_data, dict):
        msg = "Неверный формат (ожидался словарь)"
        raise BadRequest(msg)

    login = request_data.get("login")
    password = request_data.get("password")

    if login is None:
        msg = "Данные логина неизвестны"
        raise BadRequest(msg)

    if password is None:
        msg = "Данные пароля неизвестны"
        raise BadRequest(msg)

    user_db = UserDb()
    response = user_db.registration_user(request_data=request_data)

    return jsonify(response)


if __name__ == '__main__':

    @app.errorhandler(Exception)
    def special_exception_handler(error):
        """Обработка любого необработанного исключения
        для приведения в человеческий вид

        :param error: необработанная ошибка
        """
        result = {
            "message": str(error),
            "traceback": traceback.format_exc()
        }
        # если это предсказуемая ошибка, то там может быть статус ответа
        if hasattr(error, "status"):
            status = error.status
        else:
            status = 500
        return jsonify(result), status

    app.run()

