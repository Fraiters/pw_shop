from __future__ import annotations

from typing import *
from server_utils.server_settings import URL_SETTINGS


class UrlData:
    """Данные URL"""

    def __init__(self):
        url_settings = URL_SETTINGS  # type: Dict
        """словарь с данными URL"""

        self.prot = url_settings.get("prot")  # type: str
        """протокол"""
        self.host = url_settings.get("host")  # type: str
        """хост"""
        self.port = url_settings.get("port")  # type: str
        """порт"""

    def get_db_settings(self) -> UrlData:
        """Получение данных URL"""
        return UrlData()
