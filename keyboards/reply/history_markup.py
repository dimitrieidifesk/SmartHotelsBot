from typing import List, Dict

from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_utils.cities import get_cities
from utils.db_utils.database_history import get_pickle


@logger.catch
def show_commands(commands: List) -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора команд
    """
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons: List = []

    for index in commands:
        buttons.append(InlineKeyboardButton(text=f'{index}', callback_data=index[::-1]))
    buttons.append(InlineKeyboardButton(text='Закрыть историю', callback_data='close_history'))
    markup.add(*buttons)
    return markup


@logger.catch
def show_search_hotel(command: str, chat_id) -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора истории команды
    """
    date: Dict = get_pickle(chat_id)

    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons: List = []

    for city_id in date[command]:
        city_name = get_cities(city_id, 'name')
        buttons.append(InlineKeyboardButton(
            text=f'{date[command][city_id][0]} {city_name}',
            callback_data=f'final {command} {city_id}')
        )
    buttons.append(InlineKeyboardButton(text='Закрыть просмотр', callback_data='close_hotels'))
    markup.add(*buttons)
    return markup
