from uuid import uuid4
import re
from pw_shop.user.user_data import OutputUserData, InputUserData
from db_utils.base_db import BaseDb
from typing import *
from db_utils.sql_constructor import QueryCondition
from pw_shop.user.user_settings import USER_RULE
from server_utils.http_exception import BadRequest


class UserDb(BaseDb):
    """Класс для работы с таблицей пользователей (user_data)"""

    table = "user_table"  # type: str
    """сущность (таблица)"""

    def __init__(self):
        """Инициализация данных"""
        # инстанс подключения к БД
        super().__init__()

    def query_by_login(self, login: str) -> Optional[OutputUserData]:
        """Отбор записи по логину

        :param login: значение логина
        :return: запись
        """
        column = "login"
        # инстанс условия где в качестве столбца выступает - логин,
        # а в качестве значения столбца - значение логина
        query = QueryCondition(key=column, value=login)
        # добавление условия в общий список условий
        self.query_list.append(query)
        # отбор записи по всем условиям
        record = super().select_one()  # type: Dict
        # если запись не найдена, то возвращается None
        if record is None:
            return None
        output_data = OutputUserData()
        # конвертация данных из словаря в дата класс
        result = output_data.from_dict(record)

        return result

    def auth_user(self, request_data: Dict) -> Dict:
        """Авторизация пользователя

        :param request_data: данные запроса
        :return: словарь с данными ответа
        """
        # инициализация входных данных
        input_data = InputUserData().get_data(request_data)
        # отбор записи с логином из входных данных
        output_data = self.query_by_login(login=input_data.login)
        # проверка существования записи отобранной по логину
        if output_data is None:
            msg = "Неверный логин"
            raise BadRequest(msg)
        # проверка соответствия пароля логину
        if output_data.password == input_data.password:
            # конвертация выходных данных пользователя в словарь

            result = output_data.to_dict(data=output_data)
            result["token"] = output_data.get_token
        else:
            msg = "Неверный пароль"
            raise BadRequest(msg)

        return result

    def registration_user(self, request_data: Dict) -> Dict:
        """Регистрация пользователя

        :param request_data: данные запроса
        :return: словарь с данными ответа
        """
        # инициализация входных данных
        input_data = InputUserData().get_data(request_data)
        # проверка существования пользователя с логином
        user = self.query_by_login(input_data.login)
        # если пользователь с введенным логином существует, то вызывается исключение уникальный и новый
        if user is not None:
            msg = "Пользователь с таким логином уже существует"
            raise BadRequest(msg)
        output_data = OutputUserData()
        # создание пользователя (заполнение данных)
        data = self.create_user(login=input_data.login, password=input_data.password, user=output_data)
        # создание записи
        self.create(data=data)

        return data

    def create_user(self, login: str, password: str, user: OutputUserData) -> Dict[str, Any]:
        """Создание пользователя (заполнение данных)

        :param login: логин
        :param password: пароль
        :param user: данные пользователя
        """
        # генерация уникального id
        user.uuid = str(uuid4())
        # создание имени по логину
        user.name = self.create_name(login=login)
        # создание логина
        user.login = login
        # создание пароля
        user.password = password
        # создание баланса
        user.balance = 0.0
        # указание прав не авторизованного пользователя
        user.rule = USER_RULE
        # конвертация данных для создания записи
        user_dict = user.to_dict(data=user)
        return user_dict

    def create_name(self, login: str) -> str:
        """Создание имени пользователя по логину

        :param login: логин
        :return: имя
        """
        # шаблон по нахождению "собаки"
        template = r"@"
        # регулярное выражение для нахождения "собаки" в строке логина
        match = re.search(template, login)
        # если "собаки" в строке логина нет, то имя = логину с большой буквы
        if match is None:
            name = login.capitalize()
            return name
        # если "собака" есть, то отсекается правая часть логина и формируется имя
        else:
            position = login.index(template)
            name = login[:position].capitalize()
            return name


if __name__ == '__main__':
    request_data1 = {
        "login": "max@mail.ru",
        "password": "12345678",
    }

    request_data2 = {
        "login": "vlad@mail.ru",
        "password": "87654321",
    }
    user_db = UserDb()

    db_data1 = user_db.auth_user(request_data=request_data1)

    print(db_data1)
