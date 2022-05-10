from typing import Tuple

from config_data.config import USER_DATABASE
from database.pewee_database import HotelsPagination


def set_pagination(message_id: int, city_id: int, command: str) -> None:
    """
    Функция записывает в таблицу HotelsPagination users_database значения пагинации истории.
    """
    query = HotelsPagination.select().where(HotelsPagination.message_id == message_id)
    if not query.exists():
        HotelsPagination.create(message_id=message_id, command='0', city_id=0)
    row = HotelsPagination.get(HotelsPagination.message_id == message_id)
    row.command = command
    row.city_id = city_id
    row.save()
    USER_DATABASE.close()


def get_pagination(message_id: int) -> Tuple:
    """
    Функция возвращает из таблицы HotelsPagination users_database значения пагинации истории.
    """
    query = HotelsPagination.select().where(HotelsPagination.message_id == message_id)
    if query.exists:
        row = HotelsPagination.get(HotelsPagination.message_id == message_id)
        USER_DATABASE.close()
        return row.command, row.city_id
