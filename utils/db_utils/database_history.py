import datetime
import shelve
from collections import OrderedDict
from typing import Dict, Union
from loguru import logger

from config_data.config import DATA_HISTORY, NUMBER_HISTORY


@logger.catch
def get_pickle(id_chat: int) -> Union[Dict, object]:
    """
    Функция получает из файла историю запросов пользователя.
    """
    key: str = f'{id_chat}'
    with shelve.open(DATA_HISTORY, writeback=True) as file:
        if key in file:
            result: object = file[key]
            return result
        else:
            result = {}
            return result


@logger.catch
def set_pickle(id_chat: int, command: str, destination_id: int, hotel_info: str) -> None:
    """
    Функция записывает в файл историю запросов пользователя.
    """
    data_new: Dict = get_pickle(id_chat)

    if command in data_new:
        if len(data_new[command]) == NUMBER_HISTORY + 1:
            data_new[command].popitem(last=False)
    else:
        data_new[command] = OrderedDict()

    if destination_id not in data_new[command]:
        result_time: str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        data_new[command][destination_id] = [result_time]

    data_new[command][destination_id].append(hotel_info)

    with shelve.open(DATA_HISTORY, writeback=True) as file:
        key: str = f'{id_chat}'
        file[key] = data_new
