from __future__ import annotations
from typing import *

class InputUserData:
    """Входные данные пользователя (для авторизации и регистрации)"""

    def __init__(self):

        self.login = ...  # type: str
        """логин"""
        self.password = ...  # type: str
        """пароль"""
    @classmethod
    def get_data(cls, data: Dict) -> InputUserData:
        """Получить данные для авторизации или регистрации"""
        input_user_data = cls()
        input_user_data.login = data.get("login")
        input_user_data.password = data.get("password")

        return input_user_data


class OutputUserData:
    """Данные Пользователя"""
    def __init__(self):

        self.uuid = ...  # type: str
        """уникальный номер"""
        self.name = ...  # type: str
        """имя"""
        self.login = ...  # type: str
        """логин"""
        self.password = ...  # type: str
        """пароль"""
        self.balance = ...  # type: float
        """баланс"""
        self.rule = ...  # type: str
        """права"""

    @classmethod
    def from_dict(cls, data: Dict) -> OutputUserData:
        """Конвертация данных записи в данные пользователя

        :param data: словарь
        :return: данные пользователя
        """
        output_user_data = cls()
        output_user_data.uuid = data.get("uuid")
        output_user_data.name = data.get("name")
        output_user_data.login = data.get("login")
        output_user_data.password = data.get("password")
        output_user_data.balance = data.get("balance")
        output_user_data.rule = data.get("rule")

        return output_user_data

    def to_dict(self, data: OutputUserData) -> Dict:
        """Конвертация данных пользователя в словарь

        :param data: данные словаря
        :return: словарь
        """

        result = {
            "uuid": data.uuid,
            "name": data.name,
            "login": data.login,
            "password": data.password,
            "balance": data.balance,
            "rule": data.rule,
            }

        return result
