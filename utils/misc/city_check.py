import json
from typing import List, Union

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

    data = json.loads("[" + response + "]")
    sr_values = [item["sr"] for item in data]
    if sr_values:
        cities = []
        for city_apart in sr_values[0]:
            if city_apart["type"] != "CITY":
                continue
            city = city_apart["regionNames"]["shortName"]
            try:
                country = city_apart["hierarchyInfo"]["country"]["name"]
                if country:
                    city += ", " + country
            except KeyError:
                pass
            cityId = city_apart["gaiaId"]
            latitude = city_apart["coordinates"]["lat"]
            longitude = city_apart["coordinates"]["long"]
            result = {
                "city_name": city,
                "destination_id": int(cityId),
                "latitude": latitude,
                "longitude": longitude,
            }
            cities.append(result)
        add_cities(cities)
        return cities
    else:
        return False
