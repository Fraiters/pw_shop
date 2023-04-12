from psycopg2.extras import RealDictCursor, DictCursor
from db_utils.db_connection import DbConnection
from typing import *

from db_utils.sql_constructor import QueryCondition, SqlConstructor


class BaseData:
    """Базовый класс данных в БД"""
    pass


class BaseDb:
    """Базовый класс работы с таблицей в БД"""
    table = "не заданная таблица"
    """наименование таблицы"""

    def __init__(self, db: DbConnection):

        self.constructor = SqlConstructor()
        self.db = ...  # type: DbConnection
        """подключение к БД"""

        self.query_list = []  # type: List[QueryCondition]
        """условия отбора"""

    def clear(self):
        """Очистка условий отбора"""
        self.query_list = []

    def add_query(self, key: str, value: Any, operation: str = '=', connector: str = 'AND'):
        """Добавление условия отбора

        :param key: ключ
        :param value: значение
        :param operation: операция сравнения
        :param connector: соединитель
        """
        # если условие будет первым, то соединитель не используется
        if len(self.query_list) == 0:
            connector = None

        condition = QueryCondition(key=key, value=value, operation=operation, connector=connector)
        self.query_list.append(condition)

    def select_all(self) -> List[Dict]:
        """Выбор всех строк (с условием и без) в таблице"""

        sql = SqlConstructor()
        # команда select с учетом указанной таблицы
        select_sql = sql.select(table=self.table)
        # если длина списка условий не нуль
        if len(self.query_list) != 0:
            # то в запросе используется команда where
            where_sql = sql.where(query_list=self.query_list)
            # объединение select и where
            sql_command = sql.join_command(first_command=select_sql, second_command=where_sql)
        else:
            sql_command = select_sql

        # открытие соединения с БД
        con = DbConnection().connect()
        # открытие курсора для обращения к БД
        cursor = con.cursor(cursor_factory=RealDictCursor)
        # выполнение запроса
        cursor.execute(sql_command)

        # выбор всех нужных строк с учетом условий
        db_data = cursor.fetchall()
        # закрытие курсора
        cursor.close()
        # закрытие соединения с БД
        con.close()
        print("Соединение с БД закрыто")
        # очистка всех условий
        self.clear()
        # конвертация данных
        result = self.convert_to_dict(data=db_data)

        return result

    def select_one(self) -> Dict:
        """Выбор одной строки (с условием и без) в таблице"""

        result = self.select_all()
        if len(result) != 0:
            return result[0]

    def convert_to_dict(self, data: RealDictCursor) -> List[Dict]:
        """Конвертация из RealDictCursor в список словарей

        :param data: данные RealDictCursor
        :return: список словарей
        """

        result = []
        for item in data:
            dict_data = dict(item)
            result.append(dict_data)

        return result

    def create(self, data: BaseData):
        pass

    def update(self, data: Dict[str, Any]):
        pass

    def query_in(self, field: str, value: List):
        pass
