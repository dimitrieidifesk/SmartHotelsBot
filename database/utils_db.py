from typing import List, Union

from loguru import logger

from config_data.config import USER_DATABASE
from database.pewee_database import UserStates, CurrentRequests, Cities


@logger.catch
def get_state(current_id: int) -> str:
    """
    Функция возвращает значение состояния пользователя из таблицы UserStates users_database.
    """
    query = UserStates.select().where(UserStates.chat_id == current_id)
    if query.exists():
        row = UserStates.get(UserStates.chat_id == current_id)
        USER_DATABASE.close()
        return row.states
    else:
        USER_DATABASE.close()
        return '0'


@logger.catch
def set_state(current_id: int, user_states: str) -> None:
    """
    Функция устанавливает состояние пользователя в таблицу UserStates users_database.
    """
    query = UserStates.select().where(UserStates.chat_id == current_id)
    if query.exists():
        row = UserStates.get(UserStates.chat_id == current_id)
        row.states = user_states
        row.save()
        USER_DATABASE.close()
    else:
        UserStates.create(chat_id=current_id, states=user_states)
        USER_DATABASE.close()


@logger.catch
def set_current_requests(
        current_id: int, default: bool = False,
        current_command: str = None, current_destination_id: int = None,
        current_hotels: int = None, current_images: int = None,
        current_check_in: str = None, current_check_out: str = None
) -> None:
    """
    Функция с переданным параметром default=True устанавливает
    в таблице CurrentRequests users_database дефолтные значения.
    Без default записывает в колонки таблицы переданные значения.
    """
    if default:
        query = CurrentRequests.select().where(CurrentRequests.chat_id == current_id)
        if query.exists():
            row = CurrentRequests.delete().where(CurrentRequests.chat_id == current_id)
            row.execute()
            USER_DATABASE.close()
            return
        else:
            USER_DATABASE.close()
            return
    query = CurrentRequests.select().where(CurrentRequests.chat_id == current_id)
    if not query.exists():
        CurrentRequests.create(
            chat_id=current_id,
            command='0',
            destination_id=0,
            hotels=0,
            images=0,
            check_in='0',
            check_out='0'
        )
    row = CurrentRequests.get(CurrentRequests.chat_id == current_id)
    if current_command:
        row.command = current_command
    if current_destination_id:
        row.destination_id = current_destination_id
    if current_hotels:
        row.hotels = current_hotels
    if current_images:
        row.images = current_images
    if current_check_in:
        row.check_in = current_check_in
    if current_check_out:
        row.check_out = current_check_out
    row.save()
    USER_DATABASE.close()


@logger.catch
def get_current_requests(current_id: int, column: str) -> Union[str, int]:
    """
    Функция возвращает значения колонок из таблицы CurrentRequests users_database.
    """
    query = CurrentRequests.select().where(CurrentRequests.chat_id == current_id)
    if query.exists():
        row = CurrentRequests.get(CurrentRequests.chat_id == current_id)
        if column == 'command':
            USER_DATABASE.close()
            return row.command
        elif column == 'destination_id':
            USER_DATABASE.close()
            return row.destination_id
        elif column == 'hotels':
            USER_DATABASE.close()
            return row.hotels
        elif column == 'images':
            USER_DATABASE.close()
            return row.images
        elif column == 'check_in':
            USER_DATABASE.close()
            return row.check_in
        elif column == 'check_out':
            USER_DATABASE.close()
            return row.check_out
    else:
        USER_DATABASE.close()
        return '0'


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


@logger.catch
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
