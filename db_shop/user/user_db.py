from db_shop.user.user_data import OutputUserData, InputUserData
from db_utils.base_db import BaseDb
from typing import *
from db_utils.db_connection import DbConnection
from db_utils.sql_constructor import QueryCondition


class UserDb(BaseDb):
    """Класс для работы с таблицей пользователей (user_data)"""

    table = "user_table"  # type: str
    """сущность (таблица)"""

    def __init__(self):
        """Инициализация данных"""
        # инстанс подключения к БД
        db = DbConnection()
        super().__init__(db=db)

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

        if record is None:
            msg = "Неверный логин"
            raise Exception(msg)

        output_data = OutputUserData()
        result = output_data.from_dict(record)

        return result

    def auth_user(self, request_data: Union[Dict, List[Dict]]) -> Dict:
        """Регистрация пользователя

        :param request_data: данные запроса
        :return: словарь с данными ответа
        """
        # инициализация входных данных
        input_data = InputUserData().get_data(request_data)
        # отбор записи с логином из входных данных
        output_data = self.query_by_login(login=input_data.login)
        # проверка соответствия пароля логину
        if output_data.password == input_data.password:
            # конвертация выходных данных пользователя в словарь
            result = output_data.to_dict(data=output_data)
        else:
            msg = "Неверный пароль"
            raise Exception(msg)

        return result


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



