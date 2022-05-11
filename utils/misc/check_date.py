from datetime import date

from loguru import logger


@logger.catch
def get_date(convert_date: str) -> date:
    """
    Функция конвертирует полученную дату в строковом выражении и возвращает объект класса date
    """
    convert_date = convert_date.split('-')
    result = date(int(convert_date[0]), int(convert_date[1]), int(convert_date[2]))
    return result


@logger.catch
def check_date(date_one: str, date_two: str) -> int:
    """
    Функция сравнивает две даты
    """
    date_one = get_date(date_one)
    date_two = get_date(date_two)
    result = (date_two - date_one).days
    return result
