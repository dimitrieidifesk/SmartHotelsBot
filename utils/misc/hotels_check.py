import re
from typing import Union, List

from loguru import logger
from requests import Response

from utils.db_utils.current_requests import get_current_requests
from utils.hotel_patterns import *
from utils.misc.check_distance import check_distance


@logger.catch
def hotels_check(response_api: Union[Response, bool], chat_id=None) -> Union[List, bool]:
    """
    Функция выбирает необходимую информацию и возвращает список отелей.
    """
    distance_min: int = 0
    distance_max: int = 0
    response: str = response_api.text
    if chat_id:
        distance_min += get_current_requests(chat_id, "distance_min")
        distance_max += get_current_requests(chat_id, "distance_max")
    find = re.search(PATTERN_HOTELS_RESULT, response)
    if find:
        hotels_all = re.findall(PATTERN_HOTEL_APART, find.group(0))
        hotels: List = []
        for hotel_apart in hotels_all:
            name = re.search(PATTERN_NAME_HOTEL, hotel_apart)
            if name:
                name = name.group(0)
            else:
                continue
            address = ' '
            country = re.search(PATTERN_COUNTRY, hotel_apart)
            if country:
                address += country.group(0)
            locality = re.search(PATTERN_LOCALITY, hotel_apart)
            if locality:
                address += ', ' + locality.group(0)
            street = re.search(PATTERN_STREET, hotel_apart)
            if street:
                address += ', ' + street.group(0)
            id_hotel = re.search(PATTERN_ID_HOTEL, hotel_apart)
            if id_hotel:
                id_hotel = id_hotel.group(0)
            else:
                continue
            day_price = re.search(PATTERN_DAY_PRICE, hotel_apart)
            if day_price:
                day_price = day_price.group(0)
            else:
                continue
            distance_for_center = re.search(PATTERN_DISTANCE, hotel_apart)
            if distance_for_center:
                distance_for_center = distance_for_center.group(0)
                if chat_id:
                    if not check_distance(distance_for_center, distance_min, distance_max):
                        continue
            else:
                if chat_id:
                    continue
                distance_for_center = 0
            latitude = re.search(PATTERN_LATITUDE, hotel_apart)
            if latitude:
                latitude = latitude.group(0)
            else:
                latitude = 0
            longitude = re.search(PATTERN_LONGITUDE, hotel_apart)
            if longitude:
                longitude = longitude.group(0)
            else:
                longitude = 0
            star_rating = re.search(PATTERN_STAR_RATING, hotel_apart)
            if star_rating:
                star_rating = star_rating.group(0)
            else:
                star_rating = 0

            result = {
                'hotel_name': name, "address": address, 'id_hotels': id_hotel,
                'day_price': day_price, 'latitude': latitude, "longitude": longitude,
                'star_rating': star_rating, 'distance': distance_for_center
            }
            for structure in hotels:
                if result['id_hotels'] in structure:
                    return hotels
                else:
                    pass
            hotels.append(result)
        return hotels
    else:
        return False
