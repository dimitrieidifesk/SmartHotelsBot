import os
import pickle
import datetime
from collections import OrderedDict
from typing import Dict

from loguru import logger

from config_data.config import DATA_HISTORY, NUMBER_HISTORY


@logger.catch
def create_pickle() -> None:
    """Функция создает пустой словарь и сохраняет его в файловой системе"""
    if not os.path.exists(DATA_HISTORY):
        data: Dict = {}
        with open(DATA_HISTORY, 'wb') as file:
            pickle.dump(data, file)


@logger.catch
def get_pickle() -> Dict:
    with open(DATA_HISTORY, 'rb') as file:
        data_new: Dict = pickle.load(file)

        return data_new


@logger.catch
def set_pickle(id_chat: int, command: str, destination_id: int, hotel_info: str) -> None:
    """
    Функция записывает в файл историю запросов.
    """
    with open(DATA_HISTORY, 'rb') as file:
        data_new: Dict = pickle.load(file)

    if id_chat in data_new:
        if command in data_new[id_chat]:
            if len(data_new[id_chat][command]) == NUMBER_HISTORY + 1:
                data_new[id_chat][command].popitem(last=False)
        else:
            data_new[id_chat][command] = OrderedDict()
    else:
        data_new[id_chat] = {command: OrderedDict()}
    if destination_id not in data_new[id_chat][command]:
        result_time: str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        data_new[id_chat][command][destination_id] = [result_time]

    data_new[id_chat][command][destination_id].append(hotel_info)

    with open(DATA_HISTORY, 'wb') as file:
        pickle.dump(data_new, file)
