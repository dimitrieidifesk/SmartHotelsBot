from typing import Union, Dict

from geopy.distance import distance
from loguru import logger

from utils.db_utils.cities import get_cities
from utils.db_utils.current_requests import get_current_requests


@logger.catch
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
