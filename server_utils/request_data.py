from flask import request
from server_utils.http_exception import BadRequest


def get_json():
    result = request.get_json(force=True)
    return result


def get_request_data():
    """Получение данных из запроса

    :return: словарь с данными из запроса
    """
    result = {}

    if request.method == 'POST':
        # берется json из тела
        result = get_json()

    elif request.method == 'GET':
        # берутся аргументы из url
        result = request.args

    return result


def get_request_file() -> bytes:
    """Получение файла из запроса

    :return: данные файла
    """
    content_type = request.headers.get('Content-Type', None)  # type: str
    # если прислали форму с файлом (данные из запроса request.data взять не получится)
    if content_type is not None and content_type.startswith('multipart/form-data'):
        # берется файл из формы в запросе
        file_form = request.files['files[]']
        # читаются данные файла из потока внутри формы
        result = file_form.stream.read()
    # в остальных случаях отдаются данные из запроса
    else:
        result = request.data
    return result
