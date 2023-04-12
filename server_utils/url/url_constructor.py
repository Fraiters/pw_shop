from server_utils.url.url_data import UrlData


class UrlConstructor:
    """Конструктор URL"""
    def __init__(self):
        self.url = UrlData()  # type: UrlData
        """создание url"""

    def construct(self) -> str:
        """Сборка URL-адреса"""
        url = self.url
        prot = url.prot
        host = url.host
        port = url.port

        result = "".join((prot, '://', host, ':', port))

        return result


if __name__ == '__main__':

    url = UrlConstructor()

    result = url.construct()

    print(result)
