from typing import List

from loguru import logger
from telebot.types import CallbackQuery, Message

from handlers.default_handlers.from_date import from_date
from handlers.default_handlers.history import send_character_page
from keyboards.other.calendar import calendar_date_from, calendar_date_before
from keyboards.reply.common_markup import markup_choice_date_from, markup_choice_cancel, markup_choice_date_before
from keyboards.reply.common_markup import markup_before_cancel
from loader import bot
from utils.db_utils.cities import get_cities
from utils.db_utils.current_requests import set_current_requests, get_current_requests
from utils.db_utils.state import set_state
from utils.misc.calendar_call import calendar_call


@logger.catch
def calendar_calldata(call: CallbackQuery) -> None:
    """
    Функция обрабатывает нажатия кнопок календаря, выбора города
    """
    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id
    message: Message = call.message

    # TODO можно заменить на if elif else ? часть условий

    if call_data.startswith(calendar_date_from.prefix):
        text_choice: str = 'Вы выбрали дату въезда:'
        calendar_call(
            call, calendar_date_from.sep, text_choice, markup_choice_date_from(), markup_choice_cancel(), 'check_in'
        )

    if call_data.startswith(calendar_date_before.prefix):
        text_choice: str = 'Вы выбрали дату выезда:'
        calendar_call(
            call, calendar_date_before.sep, text_choice, markup_choice_date_before(), markup_before_cancel(),
            'check_out'
        )
    if call_data.startswith('id'):
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        info_all: List = call_data.split()

        result: str = get_cities(int(info_all[1]), "name")
        bot.send_message(chat_id, f"Вы выбрали:\n{result}")
        set_current_requests(chat_id, current_destination_id=int(info_all[1]))
        if get_current_requests(chat_id, "command") == 'bestdeal':
            set_state(chat_id, states='price_min')
            bot.send_message(chat_id, "Введите желаемую минимальную стоимость за ночь в рублях (целое число):")
        else:
            set_state(chat_id, states='date_from')
            from_date(message)

    if call_data.startswith('final'):
        bot.delete_message(chat_id, message_id)
        info_all: List = call_data.split()
        send_character_page(message, command=info_all[1], city_id=int(info_all[2]))
