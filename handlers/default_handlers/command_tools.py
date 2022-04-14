from datetime import datetime, timedelta, date
from typing import Dict, Union, List

import telebot
from loguru import logger
from requests import Response
from telebot.types import Message, InputMediaPhoto
from validator_collection import checkers

from config_data.config import DEFAULT_COMMANDS
from database.utils_db import get_state, set_current_requests, get_current_requests, set_state
from keyboards.other.calendar import calendar, calendar_date_from, calendar_date_before
from keyboards.reply.lowprice_markup import city_markup, markup_choice_city, markup_choice_photo, markup_start
from loader import bot
from utils.misc.common_tools import get_api, city_check, get_date, hotels_check, price_all_days, \
    get_distance_for_center, showing_photos, check_date


@bot.message_handler(func=lambda message: 'city' in get_state(message.chat.id))
@logger.catch
def find_a_city(message: Message) -> None:
    """Функция осуществляет поиск города и предоставляет пользователю выбрать из результатов поиска.
    """
    url: str = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring: Dict = {"query": message.text, "locale": "ru_RU", "currency": "RUB"}
    result_requests: Union[Response, bool] = get_api(url, querystring)
    result_check: Union[List, bool] = city_check(result_requests)
    if result_check:
        bot.send_message(
            message.chat.id, 'Уточните, пожалуйста:',
            reply_markup=city_markup(result_check)
        )
    else:
        bot.send_message(message.chat.id, 'Увы ничего не нашлось, попробуем еще?', reply_markup=markup_choice_city())


@bot.message_handler(func=lambda message: 'date_from' in get_state(message.chat.id))
@logger.catch
def from_date(message: Message) -> None:
    """
    Функция-хэндлер предлагает пользователю выбор даты заезда.
    """
    now: datetime = datetime.now()
    bot.send_message(
        message.chat.id,
        "Выберите дату въезда в гостиницу",
        reply_markup=calendar.create_calendar(
            name=calendar_date_from.prefix,
            year=now.year,
            month=now.month,
        ),
    )


@bot.message_handler(func=lambda message: 'date_before' in get_state(message.chat.id))
@logger.catch
def before_date(message: Message) -> None:
    """
    Функция-хэндлер предлагает пользователю выбор дату выезда.
    """
    now: datetime = datetime.now()
    bot.send_message(
        message.chat.id,
        "Выберите дату выезда из гостиницы",
        reply_markup=calendar.create_calendar(
            name=calendar_date_before.prefix,
            year=now.year,
            month=now.month,
        ),
    )


@logger.catch
def check_dates(chat_id: int) -> None:
    """
    Функция проверяет введенные пользователем даты.
    """
    bot.send_message(chat_id, 'Проверяю даты...')
    check: bool = True
    date_in: Union[str, date] = get_current_requests(chat_id, "check_in")
    date_out: str = get_current_requests(chat_id, "check_out")
    date_today: str = datetime.today().strftime('%Y-%m-%d')

    if check_date(date_today, date_in) < 0:
        bot.send_message(
            chat_id, f'Дата въезда установлена на сегодня: {date_today}'
        )
        set_current_requests(chat_id, current_check_in=date_today)
        check: bool = False

    date_in = get_current_requests(chat_id, "check_in")

    if check_date(date_in, date_out) <= 0:
        date_in = get_date(date_in)
        date_in = date_in + timedelta(days=1)
        date_in = date_in.strftime('%Y-%m-%d')
        bot.send_message(
            chat_id, f'Дата выезда установлена на следующий день: {date_in}'
        )
        set_current_requests(chat_id, current_check_out=date_in)
        check = False
    if check:
        bot.send_message(chat_id, 'Все ок.')
    bot.send_message(chat_id, 'Напишите количество отелей для показа (1-25):')
    set_state(chat_id, 'hotels_number')


@bot.message_handler(func=lambda message: 'hotels_number' in get_state(message.chat.id))
@logger.catch
def hotels_number_choice(message: Message) -> None:
    """
    Функция-хэндлер устанавливает количество показываемых отелей.
    """
    if message.text.isdigit():
        number: int = int(message.text)
        if number > 25 or number < 1:
            bot.send_message(
                message.chat.id, 'Некорректный ввод.\nБудут показаны не более 25 отелей')
            set_current_requests(message.chat.id, current_hotels=10)
        else:
            bot.send_message(
                message.chat.id, f'Будут показаны {number} отелей')
            set_current_requests(message.chat.id, current_hotels=number)
    else:
        bot.send_message(message.chat.id, 'Некорректный ввод.\nБудут показаны не более 25 отелей')
        set_current_requests(message.chat.id, current_hotels=10)

    bot.send_message(message.chat.id, 'Показывать фотографии отелей?', reply_markup=markup_choice_photo())


@bot.message_handler(func=lambda message: 'choice_photo_number' in get_state(message.chat.id))
@logger.catch
def choice_photo_number(message: Message) -> None:
    """
        Функция-хэндлер устанавливает количество показываемых фотографий.
        """
    if message.text.isdigit():
        number: int = int(message.text)
        if number > 10 or number < 1:
            bot.send_message(
                message.chat.id, 'Некорректный ввод.\nБудут показаны не более 10 фотографий')
            set_current_requests(message.chat.id, current_images=10)
            set_state(message.chat.id, '0')
        else:
            bot.send_message(
                message.chat.id, f'Будут показаны {number} фотографий')
            set_current_requests(message.chat.id, current_images=number)
            set_state(message.chat.id, '0')
            if get_current_requests(message.chat.id, "command") == 'lowprice':
                request_hotels(message.chat.id, 'PRICE')
            elif get_current_requests(message.chat.id, "command") == 'highprice':
                request_hotels(message.chat.id, 'PRICE_HIGHEST_FIRST')

    else:
        bot.send_message(message.chat.id, 'Некорректный ввод.\nБудут показаны не более 10 фотографий')
        set_current_requests(message.chat.id, current_images=10)
        set_state(message.chat.id, '0')
        if get_current_requests(message.chat.id, "command") == 'lowprice':
            request_hotels(message.chat.id, 'PRICE')
        elif get_current_requests(message.chat.id, "command") == 'highprice':
            request_hotels(message.chat.id, 'PRICE_HIGHEST_FIRST')


@logger.catch
def request_hotels(chat_id: int, sort: str) -> None:
    """
    Функция осуществляет поиск отелей по заданным пользователем параметрам и отправляет результаты.
    """

    bot.send_message(chat_id, text="Ищем отели, подходящие вашему запросу...")
    url: str = "https://hotels4.p.rapidapi.com/properties/list"
    destination_id: int = get_current_requests(chat_id, "destination_id")
    check_in: str = get_current_requests(chat_id, "check_in")
    check_out: str = get_current_requests(chat_id, "check_out")
    hotels_count: int = get_current_requests(chat_id, "hotels")

    querystring: Dict = {
        f"destinationId": destination_id, "pageNumber": "1", "pageSize": hotels_count, "check_in": check_in,
        "checkOut": check_out, "adults1": "1", "sortOrder": {sort}, "locale": "ru_RU", "currency": "RUB"
    }
    response_api: Response = get_api(url, querystring)

    if not response_api:
        bot.send_message(chat_id, text="В городе ничего не найдено.")
        return
    else:
        hotels: Union[List, bool] = hotels_check(response_api)
        if not hotels:
            bot.send_message(chat_id, text="В городе ничего не найдено.")
            return

    date_in: str = get_current_requests(chat_id, "check_in")
    date_out: str = get_current_requests(chat_id, "check_out")
    days_all: int = price_all_days(date_in, date_out)
    show_photo: int = get_current_requests(chat_id, "images")
    for hotel in hotels:
        price: str = hotel['day_price'].replace(',', '').split()
        if days_all in [0, 1]:
            more_than_day = ''
        else:
            price_all: int = days_all * int(price[0])
            more_than_day: str = f"Цена за весь период: {price_all} RUB"
        if hotel['star_rating'] == '0.0' or hotel['star_rating'] is None:
            star_rating: str = ''
        else:
            star_rating = f", Рейтинг: {hotel['star_rating']} звезд(ы)."
        if hotel['distance']:
            distance_for_center: str = f"\nРасстояние до центра: {hotel['distance']}"
        else:
            result: Union[int, float] = get_distance_for_center(hotel, chat_id)
            if result:
                distance_for_center = f"\nРасстояние до центра: {round(result,1)} км"
            else:
                distance_for_center = ' '

        bot.send_message(
            chat_id, text=f"Название отеля: {hotel['hotel_name']}{star_rating}\n"
                          f"Адрес: {hotel['address']}{distance_for_center}\n"
                          f"URL: https://www.hotels.com/ho{hotel['id_hotels']}\n"
                          f"Цена за ночь: {int(price[0])} RUB\n"
                          f"{more_than_day}\n", disable_web_page_preview=True

        )

        if show_photo > 0:
            result_images: Union[bool, List] = showing_photos(hotel['id_hotels'])
            if result_images:
                bot.send_message(chat_id, text=f"Загружаю фотографии отеля: {hotel['hotel_name']}")
                medias: List = []
                for url in result_images[0:show_photo]:
                    if checkers.is_url(url):
                        medias.append(InputMediaPhoto(url))
                try:
                    bot.send_media_group(chat_id, medias)
                except telebot.apihelper.ApiTelegramException:
                    bot.send_message(chat_id, text="Упс что то пошло не так. Фото не загрузилось")

    set_current_requests(chat_id, default=True)
    bot.send_message(
        chat_id, "Выберите команду:", reply_markup=markup_start(DEFAULT_COMMANDS)
    )
    bot.send_message(chat_id, "Описание команд - /help")
