from typing import Tuple

from loguru import logger
from telebot.types import CallbackQuery

from handlers.default_handlers.history import send_character_page, send_history
from keyboards.other.calendar import calendar_date_from, calendar_date_before
from loader import bot
from utils.calldata_utils.calldata_choice_history import calldata_choice_history
from utils.calldata_utils.calldata_choice_photos import calldata_choice_photos
from utils.calldata_utils.calldata_cities import cities_call
from utils.calldata_utils.calldata_commands import commands_call
from utils.calldata_utils.calldata_dates import calldata_dates
from utils.calldata_utils.calldata_prefix import calendar_calldata


@bot.callback_query_handler(func=lambda call: True)
@logger.catch
def callback_worker(call: CallbackQuery) -> None:
    """
    Функция обрабатывает нажатия на кнопки пользователем и вызывает нужную функцию
    """
    call_data = call.data
    prefix: Tuple = (calendar_date_from.prefix, calendar_date_before.prefix, "id", "final")
    commands: Tuple = ("lowprice", "highprice", "bestdeal", "history")
    user_dates: Tuple = (
        'date_from_right', 'date_from_to_change', 'date_from_cancel', 'date_from_to_continue',
        'date_before_right', 'date_before_to_change', 'date_before_cancel', 'date_before_to_continue'
    )
    choice_photos: Tuple = ("choice_photo_yes", "choice_photo_no")
    history: Tuple = ("ecirpwol", "ecirphgih", "laedtseb", "close_history", "close_hotels")
    cities: Tuple = ("city_yes", "city_no")

    if call_data in commands:
        commands_call(call)
    elif call_data in cities:
        cities_call(call)
    elif call_data.startswith(prefix):
        calendar_calldata(call)
    elif call_data in user_dates:
        calldata_dates(call)
    elif call_data in choice_photos:
        calldata_choice_photos(call)

    elif call_data in history:
        calldata_choice_history(call)

    elif call_data.split('#')[0] == 'character':
        page = int(call_data.split('#')[1])
        send_character_page(call.message, page=page)
    else:
        # "back"
        bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
        send_history(call.message)
