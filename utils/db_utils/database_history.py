import datetime
import shelve
from collections import OrderedDict
from threading import Lock
from typing import Dict, Union
from loguru import logger

from config_data.config import DATA_HISTORY, NUMBER_HISTORY


@logger.catch
def get_pickle(id_chat: int) -> Union[Dict, object]:
    """
    Функция получает из файла историю запросов пользователя.
    """
    key: str = str(id_chat)
    mutex = Lock()

    mutex.acquire()
    db = shelve.open(DATA_HISTORY)
    if key in db:
        result: object = db[key]
        db.close()
        mutex.release()
        return result
    else:
        db.close()
        mutex.release()
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

    key: str = str(id_chat)
    mutex = Lock()
    mutex.acquire()
    db = shelve.open(DATA_HISTORY)
    db[key] = data_new
    db.close()
    mutex.release()
