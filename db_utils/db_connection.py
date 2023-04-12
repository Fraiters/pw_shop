import psycopg2
from psycopg2 import Error

from db_utils.db_settings_data import DbSettingsData


class DbConnection:
    """Подключение к серверу БД"""
    def __init__(self):

        self.db_settings = DbSettingsData()  # type: DbSettingsData
        """создание настроек подключения к БД"""

    def connect(self):
        try:
            """Подключение к экземпляру БД"""
            db_settings = self.db_settings

            print("Устанавливается соединение с БД")
            return psycopg2.connect(
                database=db_settings.database,
                user=db_settings.user,
                password=db_settings.password,
                host=db_settings.host,
                port=db_settings.port
            )

        except (Exception, Error) as error:
            print("Ошибка Подключения к БД", error)

        finally:
            print("Соединение с БД прошло успешно")


if __name__ == '__main__':

    db_set = {
        "database": "pw_shop",
        "user": "postgres",
        "password": "12345678",
        "host": "localhost",
        "port": "5432"
    }

    con = DbConnection().connect()

    con.close()

