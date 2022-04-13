import datetime
import re
from collections import Counter
from datetime import date
from typing import Dict, Union, List

import requests
from geopy.distance import distance
from loguru import logger
from requests import Response

from config_data.config import RAPID_API_KEY
from database.utils_db import add_cities, get_current_requests, get_cities, set_current_requests
from keyboards.other.calendar import calendar
from loader import bot


@logger.catch
def get_api(url: str, querystring: Dict) -> Union[Response, bool]:
    """
    Функция делает запрос к API Hotels и возвращает результат.
    """
    headers: Dict = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": RAPID_API_KEY
    }

    api_response: Response = requests.request("GET", url, headers=headers, params=querystring, timeout=15)
    if api_response.status_code == requests.codes['ok']:
        return api_response

    else:
        return False


@logger.catch
def city_check(response_api: Union[Response, bool]) -> Union[List, bool]:
    """
    Функция осуществляет поиск значений в полученном ответе API.
    """
    if not response_api:
        return False
    else:
        response = response_api.text

    pattern_city_group = r'(?<="CITY_GROUP",).+?[\]]'
    pattern_city_apart = r'(?<={").[^}]*'
    pattern_city = r'(?<="name":").[^"]*'
    pattern_country = r'\w+(?=","name")'
    pattern_id = r'(?<="destinationId":")\d+'
    pattern_latitude = r'(?<="latitude":).+?(?=,)'
    pattern_longitude = r'(?<="longitude":).+?(?=,)'

    find = re.search(pattern_city_group, response)
    if find:
        cities_all = re.findall(pattern_city_apart, find.group(0))
        cities = []
        for city_apart in cities_all:
            # TODO вот тут есть вопросик. Пробовал компилить шаблоны группами, заключая в скобки. Делал как с именем
            # TODO так и без. Главное по отдельности работает, а в месте ничего не ищут. В гугле ничего не нашел
            # TODO как сразу искать по нескольким шаблонам одновременно. Может вы подскажете если, что знаете.
            city = re.search(pattern_city, city_apart)
            if city:
                city = city.group(0)
            else:
                continue
            country = re.search(pattern_country, city_apart)
            if country:
                city += ', ' + country.group(0)
            city_id = re.search(pattern_id, city_apart)
            if city_id:
                city_id = city_id.group(0)
            else:
                continue
            latitude = re.search(pattern_latitude, city_apart)
            if latitude:
                latitude = latitude.group(0)
            else:
                latitude = '0'
            longitude = re.search(pattern_longitude, city_apart)
            if longitude:
                longitude = longitude.group(0)
            else:
                longitude = '0'

            result = {'city_name': city, "destination_id": int(city_id), "latitude": latitude, "longitude": longitude}
            cities.append(result)
        add_cities(cities)
        return cities
    else:
        return False


@logger.catch
def get_date(convert_date: str) -> date:
    """
    Функция конвертирует полученную дату в строковом выражении и возвращает объект класса date
    """
    convert_date = convert_date.split('-')
    result = datetime.date(int(convert_date[0]), int(convert_date[1]), int(convert_date[2]))
    return result


@logger.catch
def check_date(date_one: str, date_two: str) -> int:
    """
    Функция сравнивает две даты
    """
    date_one = get_date(date_one)
    date_two = get_date(date_two)
    result = (date_two - date_one).days
    return result


@logger.catch
def hotels_check(response_api: Union[Response, bool]) -> Union[List, bool]:
    if not response_api:
        return False
    else:
        response = response_api.text

    pattern_hotels_result = r'(?<="results":).+(?=,"pagination":)'
    pattern_name_hotel = r'(?<="name":").[^"}]*'
    pattern_street = r'(?<="streetAddress":").[^"}]*'
    pattern_locality = r'(?<=locality":").[^"}]*'
    pattern_hotel_apart = r'(?<={"id":).*?(?:=high")'
    pattern_id_hotel = r'\d+.*?'
    pattern_country = r'(?<=countryName":").[^"}]*'
    pattern_day_price = r'(?<="current":").[^"}]*'
    pattern_distance = r'(?<="Центр города","distance":").[^"}]*'
    pattern_latitude = r'(?<="lat":).[^,}]*'
    pattern_longitude = r'(?<="lon":).[^,}]*'
    pattern_star_rating = r'(?<="starRating":).[^,}]*'

    find = re.search(pattern_hotels_result, response)
    if find:
        hotels_all = re.findall(pattern_hotel_apart, find.group(0))
        hotels = []
        for hotel_apart in hotels_all:
            name = re.search(pattern_name_hotel, hotel_apart)
            if name:
                name = name.group(0)
            else:
                continue
            address = ' '
            country = re.search(pattern_country, hotel_apart)
            if country:
                address += country.group(0)
            locality = re.search(pattern_locality, hotel_apart)
            if locality:
                address += ', ' + locality.group(0)
            street = re.search(pattern_street, hotel_apart)
            if street:
                address += ', ' + street.group(0)
            id_hotel = re.search(pattern_id_hotel, hotel_apart)
            if id_hotel:
                id_hotel = id_hotel.group(0)
            else:
                continue
            day_price = re.search(pattern_day_price, hotel_apart)
            if day_price:
                day_price = day_price.group(0)
            else:
                continue
            distance_for_center = re.search(pattern_distance, hotel_apart)
            if distance_for_center:
                distance_for_center = distance_for_center.group(0)
            else:
                distance_for_center = 0
            latitude = re.search(pattern_latitude, hotel_apart)
            if latitude:
                latitude = latitude.group(0)
            else:
                latitude = 0
            longitude = re.search(pattern_longitude, hotel_apart)
            if longitude:
                longitude = longitude.group(0)
            else:
                longitude = 0
            star_rating = re.search(pattern_star_rating, hotel_apart)
            if star_rating:
                star_rating = star_rating.group(0)
            else:
                star_rating = 0

            result = {
                'hotel_name': name, "address": address, 'id_hotels': id_hotel,
                'day_price': day_price, 'latitude': latitude, "longitude": longitude,
                'star_rating': star_rating, 'distance': distance_for_center
            }
            hotels.append(result)
        return hotels
    else:
        return False


def get_distance_for_center(structure: Dict, chat_id: int) -> Union[int, float]:
    hotel_coordinates = (structure['latitude'], structure['longitude'])
    if 0 not in hotel_coordinates:
        city_current_id = get_current_requests(chat_id, "destination_id")
        latitude_city = get_cities(city_current_id, 'latitude')
        longitude_city = get_cities(city_current_id, 'longitude')
        city_coordinates = (latitude_city, longitude_city)
        result = distance(city_coordinates, hotel_coordinates).km
        return result
    else:
        return 0


@logger.catch
def price_all_days(date_one: str, date_two: str) -> int:
    """
    Функция сравнивает две даты
    """
    date_one = date_one.split('-')
    date_two = date_two.split('-')
    date_one = date(int(date_one[0]), int(date_one[1]), int(date_one[2]))
    date_two = date(int(date_two[0]), int(date_two[1]), int(date_two[2]))

    result = date_two - date_one
    return result.days


def showing_photos(id_hotels: str) -> Union[bool, List]:
    """
    Функция получает на вход ид отеля и возвращает список полученных url фотографий отеля
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": id_hotels}
    response_api = get_api(url, querystring)

    if not response_api:
        return False
    else:
        response = response_api.text

    pattern_url_images = r'(?<="baseUrl":").[^"]*'
    url_images = re.findall(pattern_url_images, response)
    url_counter = Counter(url_images)
    url_images = list(map(lambda url_current: url_current.replace('{size}', 'y'), url_counter.keys()))
    if url_images:
        return url_images
    else:
        return False


@logger.catch
def calendar_call(call, sep, text_choice: str, markup_day, markup_cancel, edit_column: str) -> None:
    """
    Функция обрабатывает call календаря
    """
    name, action, year, month, day = call.data.split(sep)
    date_choice = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    if action == "DAY":
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f"{text_choice} {date_choice.strftime('%Y-%m-%d')}",
            reply_markup=markup_day
        )
        result = date_choice.strftime('%Y-%m-%d')
        if edit_column == 'check_in':
            set_current_requests(call.message.chat.id, current_check_in=result)
        elif edit_column == 'check_out':
            set_current_requests(call.message.chat.id, current_check_out=result)
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Хотите завершить?",
            reply_markup=markup_cancel
        )
