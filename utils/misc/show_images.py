import re
from collections import Counter
from typing import Union, List, Dict, Any

from loguru import logger

from utils.misc.get_api import get_api


@logger.catch
def showing_photos(id_hotels: str) -> Union[bool, List]:
    """
    Функция получает на вход ид отеля и возвращает список полученных url фотографий отеля
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring: Dict = {"id": id_hotels}
    response_api: Any = get_api(url, querystring)

    if not response_api:
        return False
    else:
        response = response_api.text

    pattern_url_images: str = r'(?<="baseUrl":").[^"]*'
    url_images: Any = re.findall(pattern_url_images, response)
    url_counter: Counter = Counter(url_images)
    url_images: List = list(map(lambda url_current: url_current.replace('{size}', 'y'), url_counter.keys()))
    if url_images:
        return url_images
    else:
        return False
