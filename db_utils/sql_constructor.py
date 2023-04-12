from typing import *

from db_utils.template.sql_template import TEMPL_SQL_SELECT, TEMPL_SQL_WHERE


class QueryCondition:
    """Условие отбора"""

    def __init__(self, key: str, value: Any, operation: str = '=', connector: Optional[str] = None):
        self.key = key  # type: str
        """ключ"""
        self.value = value  # type: Any
        """значение"""
        self.operation = operation  # type: str
        """операция сравнения"""
        self.connector = connector  # type: Optional[str]
        """соединитель"""


class SqlConstructor:
    """Конструктор SQL-запросов"""

    def select(self, table: str) -> str:
        """Построение select запроса

        :param table: таблица
        :return: sql select запрос
        """
        sql = TEMPL_SQL_SELECT
        # result = sql.format(table=table)

        sql_format = {
            "table": self.encode_key(table)
        }
        result = self.format_sql(sql=sql, sql_format=sql_format)

        return result

    def where(self, query_list: List[QueryCondition]) -> str:
        """Построение where запроса

        :param query_list: условия отбора
        :return: sql where запрос
        """
        sql = TEMPL_SQL_WHERE
        query = self.query(query_list=query_list)
        # result = sql.format(query=query)
        sql_format = {
            "query": query
        }

        result = self.format_sql(sql=sql, sql_format=sql_format)

        return result

    def query(self, query_list: List[QueryCondition]) -> str:
        """Построение условий отбора

        :param query_list: условия отбора
        :return: sql запрос на основе условий отбора
        """
        result = None
        # проход по всем условиям запроса
        for query in query_list:
            # если соединителя нет
            if query.connector is None:
                # заполняется sql запрос без соединителя
                cur_sql = "{key} {operation} \'{value}\'".format(
                    key=query.key,
                    operation=query.operation,
                    value=query.value
                )

            else:
                # заполняется sql запрос с соединителем
                cur_sql = "{connector} {key} {operation} \'{value}\'".format(
                    connector=query.connector,
                    key=query.key,
                    operation=query.operation,
                    value=query.value
                )

            if result is None:
                result = cur_sql
            else:
                result += cur_sql

        return result

    def join_command(self, first_command: str, second_command: str) -> str:
        """Соединение двух команд БД

        :param first_command: первая БД команда
        :param second_command: вторая БД команда
        :return: объединенная команда
        """
        result = "{first_command} {second_command}".format(first_command=first_command, second_command=second_command)

        return result

    def encode_key(self, key: str) -> str:
        """Преобразование ключа

        :param key: ключ
        :return: преобразованный ключ
        """

        return "\"{key}\"".format(key=key)

    def format_sql(self, sql: str, sql_format: Dict[str, str]) -> str:
        """Форматирование sql строки в соответствии с параметрами

        :param sql: sql-строка
        :param sql_format: параметры формата
        :return: форматированная строка sql
        """
        result = sql.format(**sql_format)

        return result


if __name__ == '__main__':
    sql_con = SqlConstructor()
    table = "user"
    key = "name"
    value = "Max"
    operation = "="
    connector = None

    query_list = [QueryCondition(key=key, value=value, operation=operation, connector=connector)]

    res1 = sql_con.select(table="user")

    print(res1)

    res2 = sql_con.query(query_list=query_list)

    print(res2)

    res3 = sql_con.where(query_list=query_list)

    print(res3)
