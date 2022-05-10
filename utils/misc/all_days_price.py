from datetime import date

from loguru import logger


@logger.catch
def price_all_days(date_one: str, date_two: str) -> int:
    """
    Функция сравнивает две даты
    """
    date_one = date_one.split('-')
    date_two = date_two.split('-')
    date_one = date(int(date_one[0]), int(date_one[1]), int(date_one[2]))
    date_two = date(int(date_two[0]), int(date_two[1]), int(date_two[2]))

    result = date_two - date_one
    return result.days
