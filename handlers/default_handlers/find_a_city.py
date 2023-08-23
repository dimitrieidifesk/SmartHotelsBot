from typing import Dict, Union, List

from loguru import logger
from requests import Response
from telebot.types import Message

from keyboards.reply.common_markup import city_markup, markup_choice_city
from loader import bot
from utils.db_utils.state import get_state, set_state
from utils.misc.city_check import city_check
from utils.misc.get_api import get_api


@bot.message_handler(func=lambda message: "city" == get_state(message.chat.id, "states"))
@logger.catch
def find_a_city(message: Message) -> None:
    """Функция осуществляет поиск города и предоставляет пользователю выбрать из результатов поиска."""
    chat_id: int = message.chat.id
    url: str = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring: Dict = {"q": message.text, "locale": "ru_RU"}
    result_requests: Union[Response, bool] = get_api(url, querystring)
    result_check: Union[List, bool] = city_check(result_requests)
    if result_check:
        current_id_message = bot.send_message(
            chat_id, "Уточните, пожалуйста:", reply_markup=city_markup(result_check)
        )
        set_state(chat_id, message_id=current_id_message.id, states="choice_cities")
    else:
        current_id_message = bot.send_message(
            chat_id, "Увы ничего не нашлось, попробуем еще??", reply_markup=markup_choice_city()
        )
        set_state(chat_id, states="choice_not_cities", message_id=current_id_message.id)
