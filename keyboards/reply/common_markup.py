from typing import List

from loguru import logger
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


@logger.catch
def markup_choice_city() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора города если не найден/
    """
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Да', callback_data='city_yes'),
        InlineKeyboardButton(text='Нет', callback_data='city_no')
    )
    return markup


@logger.catch
def city_markup(cities) -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора города.
    """
    buttons: List = []
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    for index in cities:
        buttons.append(InlineKeyboardButton(text=index['city_name'], callback_data=f'id {index["destination_id"]}'))
    markup.add(*buttons)
    return markup


@logger.catch
def markup_choice_date_before() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора даты выезда.
    """
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Все верно', callback_data='date_before_right'),
        InlineKeyboardButton(text='Изменить', callback_data='date_before_to_change')
    )
    return markup


@logger.catch
def markup_before_cancel() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора даты выезда (выход).
    """
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Завершить', callback_data='date_before_cancel'),
        InlineKeyboardButton(text='Продолжить', callback_data='date_before_to_continue')
    )
    return markup


@logger.catch
def markup_choice_date_from() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора даты въезда.
    """
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Все верно', callback_data='date_from_right'),
        InlineKeyboardButton(text='Изменить', callback_data='date_from_to_change')
    )
    return markup


@logger.catch
def markup_choice_cancel() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора даты въезда (выход).
    """
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Завершить', callback_data='date_from_cancel'),
        InlineKeyboardButton(text='Продолжить', callback_data='date_from_to_continue')
    )
    return markup


@logger.catch
def markup_start(commands) -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора команд
    """
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=4)
    buttons: List = []

    for index in commands:
        if index[0] in ('start', 'help', 'cancel'):
            continue
        buttons.append(InlineKeyboardButton(
            text=f'/{index[0]}', callback_data=index[0])
        )

    markup.add(*buttons)
    return markup


@logger.catch
def markup_choice_photo() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора даты от (выход)
    """
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Да', callback_data='choice_photo_yes'),
        InlineKeyboardButton(text='Нет', callback_data='choice_photo_no')
    )
    return markup
