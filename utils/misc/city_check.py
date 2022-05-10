import re
from typing import Union, List

from loguru import logger
from requests import Response

from utils.city_patterns import *
from utils.db_utils.cities import add_cities


@logger.catch
def city_check(response_api: Union[Response, bool]) -> Union[List, bool]:
    """
    Функция осуществляет поиск значений в полученном ответе API.
    """
    if not response_api:
        return False
    else:
        response = response_api.text

    find = re.search(PATTERN_CITY_GROUP, response)
    if find:
        cities_all = re.findall(PATTERN_CITY_APART, find.group(0))
        cities = []
        for city_apart in cities_all:
            city = re.search(PATTERN_CITY, city_apart)
            if city:
                city = city.group(0)
            else:
                continue
            country = re.search(PATTERN_COUNTRY, city_apart)
            if country:
                city += ', ' + country.group(0)
            city_id = re.search(PATTERN_ID, city_apart)
            if city_id:
                city_id = city_id.group(0)
            else:
                continue
            latitude = re.search(PATTERN_LATITUDE, city_apart)
            if latitude:
                latitude = latitude.group(0)
            else:
                latitude = '0'
            longitude = re.search(PATTERN_LONGITUDE, city_apart)
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
