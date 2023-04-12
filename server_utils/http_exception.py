
class HttpException(Exception):
    """Базовое исключение при http запросе"""
    status = 500

    def __init__(self, message: str):
        self.message = message

        super().__init__(self.message)


class BadRequest(HttpException):
    """Исключение когда пользователь отправляет некорректный запрос"""
    status = 400
