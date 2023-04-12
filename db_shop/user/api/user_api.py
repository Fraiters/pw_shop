from flask import Flask, jsonify
from db_shop.user.user_db import UserDb
from server_utils.http_exception import BadRequest
from server_utils.request_data import get_request_data
from server_utils.url.url_constructor import UrlConstructor


app = Flask(__name__)
url = UrlConstructor().construct()  # "http://127.0.0.1:5000"
auth_user = "".join((url, '/auth_user'))
print(auth_user)


@app.route('/auth_user', methods=['POST'])
def auth_user():
    """АПИ для авторизации пользователя"""
    # получаем данные запроса (логин, пароль)
    request_data = get_request_data()

    login = request_data.get("login")
    password = request_data.get("password")

    if login is None:
        msg = "Данные логина неизвестны"
        raise BadRequest(msg)

    if password is None:
        msg = "Данные пароля неизвестны"
        raise Exception(msg)

    user_db = UserDb()
    response = user_db.auth_user(request_data=request_data)

    return jsonify(response)


if __name__ == '__main__':
    app.run()

