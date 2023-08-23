from datetime import datetime
from typing import List, Union

import requests
import telebot
from config_data.config import DEFAULT_COMMANDS
from keyboards.reply.common_markup import markup_start
from loader import bot
from loguru import logger
from requests import Response
from telebot.types import InputMediaPhoto
from utils.db_utils.current_requests import get_current_requests, set_current_requests
from utils.db_utils.database_history import set_pickle
from utils.db_utils.state import get_state
from utils.misc.all_days_price import price_all_days
from utils.misc.get_api import get_api_v2
from utils.misc.get_distance import get_distance_for_center
from utils.misc.hotels_check import hotels_check
from utils.misc.show_images import showing_photos
from validator_collection import checkers


@logger.catch
def request_hotels_bestdeal(chat_id: int) -> None:
    """
    Функция осуществляет поиск отелей по заданным пользователем параметрам и отправляет результаты.
    """

    bot.send_message(chat_id, text="Ищем отели, подходящие вашему запросу...")
    url: str = "https://hotels4.p.rapidapi.com/properties/v2/list"
    destination_id: int = get_current_requests(chat_id, "destination_id")
    check_in: str = get_current_requests(chat_id, "check_in")
    check_out: str = get_current_requests(chat_id, "check_out")
    hotels_count: int = get_current_requests(chat_id, "hotels")
    user_command: str = get_current_requests(chat_id, "command")
    price_min: int = get_current_requests(chat_id, "price_min")
    price_max: int = get_current_requests(chat_id, "price_max")
    hotels: List = []

    check_in: datetime = datetime.strptime(str(check_in), "%Y-%m-%d")
    check_out: datetime = datetime.strptime(str(check_out), "%Y-%m-%d")

    data = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": f"{destination_id}"},
        "checkInDate": {"day": check_in.day, "month": check_in.month, "year": check_in.year},
        "checkOutDate": {"day": check_out.day, "month": check_out.month, "year": check_out.year},
        "rooms": [{"adults": 1}],
        "resultsStartingIndex": 0,
        "resultsSize": hotels_count,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {
            "price": {"max": price_max, "min": price_min},
            "availableFilter": "SHOW_AVAILABLE_ONLY",
        },
    }
    response_api: Response = get_api_v2(url, data)
    if not response_api:
        logger.info(f"Чат - {chat_id}, по команде bestdeal ничего не найдено")
        bot.send_message(
            chat_id,
            "В городе ничего не найдено, желаете продолжить?",
            reply_markup=markup_start(DEFAULT_COMMANDS),
        )
        bot.send_message(chat_id, "Описание команд - /help")
        return
    else:
        current_result: Union[List, bool] = hotels_check(response_api, chat_id=chat_id)
        if current_result:
            hotels.extend(current_result)

    if not hotels:
        logger.info(f"Чат - {chat_id}, по команде bestdeal ничего не найдено")
        bot.send_message(
            chat_id,
            "В городе ничего не найдено, желаете продолжить?",
            reply_markup=markup_start(DEFAULT_COMMANDS),
        )
        bot.send_message(chat_id, "Описание команд - /help")
        return

    date_in: str = get_current_requests(chat_id, "check_in")
    date_out: str = get_current_requests(chat_id, "check_out")
    days_all: int = price_all_days(date_in, date_out)
    show_photo: int = get_current_requests(chat_id, "images")
    count_hotels: int = 0

    logger.info(f"Чат - {chat_id}, по команде bestdeal отправляются результаты поиска")
    for hotel in hotels:
        if count_hotels == hotels_count:
            break
        count_hotels += 1
        price: str = hotel["day_price"].replace(",", "").split()
        if days_all in [0, 1]:
            more_than_day = ""
        else:
            price_all: int = days_all * int(price[0][1::])
            more_than_day: str = f"Цена за весь период: {price_all} RUB"
        if hotel["star_rating"] == "0.0" or hotel["star_rating"] is None:
            star_rating: str = ""
        else:
            star_rating = f", Рейтинг: {hotel['star_rating']} звезд(ы)."
        if hotel["distance"]:
            distance_for_center: str = f"\nРасстояние до центра: {hotel['distance']}"
        else:
            result: Union[int, float] = get_distance_for_center(hotel, chat_id)
            if result:
                distance_for_center = f"\nРасстояние до центра: {round(result,1)} км"
            else:
                distance_for_center = " "

        hotel_info = (
            f"Название отеля: {hotel['hotel_name']}{star_rating}\n"
            f"Адрес: {hotel['address']}{distance_for_center}\n"
            f"URL: https://www.hotels.com/h{hotel['id_hotels']}.Hotel-Information\n"
            f"Цена за ночь: {price[0]}\n"
            f"{more_than_day}\n"
        )
        result_images: Union[bool, List] = showing_photos(hotel["id_hotels"])
        if len(result_images) > 0:
            medias: List = []
            count: bool = False
            for url in result_images[0:show_photo]:
                if checkers.is_url(url):
                    if not count:
                        medias.append(InputMediaPhoto(url, caption=hotel_info))
                        count = True
                    else:
                        medias.append(InputMediaPhoto(url))
            if get_state(chat_id, "states") == "send_result":
                set_pickle(chat_id, user_command, destination_id, hotel_info)
                try:
                    bot.send_media_group(chat_id, medias)
                except (telebot.apihelper.ApiTelegramException, requests.exceptions.ReadTimeout):
                    bot.send_message(
                        chat_id,
                        "Упс что то пошло не так. Фото не загрузилось\n" + hotel_info,
                        disable_web_page_preview=True,
                    )
            else:
                return
        else:
            if get_state(chat_id, "states") == "send_result":
                set_pickle(chat_id, user_command, destination_id, hotel_info)
                bot.send_message(chat_id, hotel_info, disable_web_page_preview=True)
            else:
                return
    if get_state(chat_id, "states") == "send_result":
        set_current_requests(chat_id, default=True)
        bot.send_message(
            chat_id,
            "Поиск окончен, желаете продолжить?",
            reply_markup=markup_start(DEFAULT_COMMANDS),
        )
        bot.send_message(chat_id, "Описание команд - /help")
