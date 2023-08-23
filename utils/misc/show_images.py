import json
import re
from collections import Counter
from typing import Any, Dict, List, Union

from loguru import logger
from utils.misc.get_api import get_api_v2


@logger.catch
def showing_photos(id_hotels: str) -> Union[bool, List]:
    """
    Функция получает на вход ид отеля и возвращает список полученных url фотографий отеля
    """
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": str(id_hotels),
    }
    response_api: Any = get_api_v2(url, payload)

    if not response_api:
        return False
    else:
        response = response_api.text

    data = json.loads("[" + response + "]")
    sr_values = [item["data"]["propertyInfo"]["propertyGallery"]["images"] for item in data]
    url_images: List = []
    for i, image in enumerate(sr_values[0]):
        if i > 10:
            continue
        image_url = image["image"]["url"]
        url_images.append(image_url)
    if url_images:
        return url_images
    else:
        return False
