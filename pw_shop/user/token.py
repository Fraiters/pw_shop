import secrets


class Token:
    """Класс работы с токеном"""
    access_token = ...  # type: str
    # refresh_token = ...  # type: str

    def generate(self) -> str:
        """Генерация токена

        :return:
        """
        self.access_token = secrets.token_hex(16)

        return self.access_token
