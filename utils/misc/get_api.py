from typing import Dict, Union

import requests
from loguru import logger
from requests import Response

from config_data.config import RAPID_API_KEY


@logger.catch
def get_api(url: str, querystring: Dict) -> Union[Response, bool]:
    """
    Функция делает запрос к API Hotels и возвращает результат.
    """
    headers: Dict = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": RAPID_API_KEY
    }
    for _ in range(3):
        try:
            api_response: Response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
            if api_response.status_code == requests.codes['ok']:
                return api_response
        except requests.exceptions.Timeout as error:
            logger.error(f'Ошибка таймаута {error}')
        except ConnectionError as error:
            logger.error(f'Ошибка соединения {error}')
    else:
        return False
