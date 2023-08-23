from typing import Dict, Union

import requests
from config_data.config import RAPID_API_KEY
from loguru import logger
from requests import Response


@logger.catch
def get_api(url: str, querystring: Dict) -> Union[Response, bool]:
    """
    Функция делает GET запрос к API Hotels и возвращает результат.
    """
    headers: Dict = {"X-RapidAPI-Host": "hotels4.p.rapidapi.com", "X-RapidAPI-Key": RAPID_API_KEY}
    for _ in range(1):
        try:
            api_response: Response = requests.request(
                "GET", url, headers=headers, params=querystring, timeout=10
            )
            if api_response.status_code == requests.codes["ok"]:
                return api_response
        except requests.exceptions.Timeout as error:
            logger.error(f"Ошибка таймаута {error}")
        except ConnectionError as error:
            logger.error(f"Ошибка соединения {error}")
    else:
        return False


@logger.catch
def get_api_v2(url: str, data: Dict) -> Union[Response, bool]:
    """
    Функция делает POST запрос к API Hotels с обновленными параметрами и возвращает результат.
    """
    headers: Dict = {
        "content-type": "application/json",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": RAPID_API_KEY,
    }
    for _ in range(1):
        try:
            api_response: Response = requests.request(
                "POST", url, headers=headers, json=data, timeout=20
            )
            if api_response.status_code == requests.codes["ok"]:
                return api_response
        except requests.exceptions.Timeout as error:
            logger.error(f"Ошибка таймаута {error}")
        except ConnectionError as error:
            logger.error(f"Ошибка соединения {error}")
    else:
        return False
