from typing import List

from loguru import logger

from config_data.config import USER_DATABASE
from database.pewee_database import Cities


@logger.catch
def add_cities(cities: List) -> None:
    """
    Функция записывает в таблицу Cities users_database найденные города.
    """
    for index in cities:
        query = Cities.select().where(Cities.destination_id == index['destination_id'])
        if not query.exists():
            Cities.create(destination_id=index['destination_id'], name='0', latitude='0', longitude='0')
        row = Cities.get(Cities.destination_id == index['destination_id'])
        row.name = index['city_name']
        row.latitude = index['latitude']
        row.longitude = index['longitude']
        row.save()
    USER_DATABASE.close()


def get_cities(current_destination_id: int, column: str) -> str:
    """
    Функция возвращает из таблицы Cities users_database значения переданной колонки.
    """
    query = Cities.select().where(Cities.destination_id == current_destination_id)
    if query.exists:
        row = Cities.get(Cities.destination_id == current_destination_id)
        if column == 'name':
            USER_DATABASE.close()
            return row.name
        elif column == 'latitude':
            USER_DATABASE.close()
            return row.latitude
        elif column == 'longitude':
            USER_DATABASE.close()
            return row.longitude
    else:
        USER_DATABASE.close()
        return '0'
