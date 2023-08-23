import json
from typing import List, Union

from loguru import logger
from requests import Response
from utils.db_utils.current_requests import get_current_requests
from utils.hotel_patterns import *
from utils.misc.check_distance import check_distance
from utils.misc.get_api import get_api_v2


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
    data = json.loads("[" + response + "]")
    find = [item["data"]["propertySearch"]["properties"] for item in data]
    if find:
        hotels: List = []
        for hotel in find[0]:
            name = hotel["name"]
            id_hotel = hotel["id"]
            url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
            payload = {
                "currency": "RUB",
                "eapid": 1,
                "locale": "ru_RU",
                "siteId": 300000001,
                "propertyId": str(id_hotel),
            }
            hotel_detail_info: Response = get_api_v2(url, payload)
            hotel_detail_info = json.loads("[" + hotel_detail_info.text + "]")
            hotel_detail_info = hotel_detail_info[0]["data"]["propertyInfo"]

            address = hotel_detail_info["summary"]["location"]["address"]["addressLine"]
            day_price = hotel["price"]["lead"]["formatted"]
            latitude = hotel["mapMarker"]["latLong"]["latitude"]
            longitude = hotel["mapMarker"]["latLong"]["longitude"]
            star_rating = hotel["star"]
            distance_for_center = hotel["destinationInfo"]["distanceFromDestination"]["value"]
            result = {
                "hotel_name": name,
                "address": address,
                "id_hotels": id_hotel,
                "day_price": day_price,
                "latitude": latitude,
                "longitude": longitude,
                "star_rating": star_rating,
                "distance": distance_for_center,
            }
            hotels.append(result)
        return hotels
    else:
        return False
