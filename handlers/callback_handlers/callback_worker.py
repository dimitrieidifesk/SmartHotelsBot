from typing import List

from loguru import logger
from telebot.types import CallbackQuery

from database.utils_db import get_cities, set_current_requests, set_state, get_current_requests
from handlers.default_handlers.cancel import any_state
from handlers.default_handlers.high_price import send_highprice
from handlers.default_handlers.low_price import send_lowprice
from keyboards.other.calendar import calendar_date_before, calendar_date_from
from keyboards.reply.lowprice_markup import markup_choice_date_before, markup_before_cancel, markup_choice_date_from, \
    markup_choice_cancel
from loader import bot
from utils.misc.common_tools import calendar_call
from handlers.default_handlers.command_tools import from_date, before_date, request_hotels, check_dates


@bot.callback_query_handler(func=lambda call: True)
@logger.catch
def callback_worker(call: CallbackQuery) -> None:
    """
    Функция обрабатывает нажатия на кнопки пользователем и вызывает нужную функцию
    """

    if call.data == "lowprice":  # обработка кнопок от выбора команд
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text=f"Вы выбрали /{call.data}")
        send_lowprice(call.message)
    if call.data == "highprice":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text=f"Вы выбрали /{call.data}")
        send_highprice(call.message)
    if call.data == "bestdeal":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text=f"Вы выбрали /{call.data}")
        bot.send_message(call.message.chat.id, text="В разработке")  # TODO В разработке
    if call.data == "history":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text=f"Вы выбрали /{call.data}")
        bot.send_message(call.message.chat.id, text="В разработке")  # TODO В разработке

    if call.data == "city_yes":   # обработка кнопок от выбора города если не найден
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text=f"Вы выбрали 'Да'")
        send_lowprice(call.message)
    if call.data == "city_no":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text=f"Вы выбрали 'Нет'")
        any_state(call.message)

    if call.data.startswith('id'):  # обработка кнопок от выбора города если найден
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        info_all: List = call.data.split()

        result: str = get_cities(int(info_all[1]), "name")
        bot.send_message(call.message.chat.id, text=f"Вы выбрали:\n{result}")
        set_current_requests(call.message.chat.id, current_destination_id=int(info_all[1]))
        set_state(call.message.chat.id, 'date_from')
        from_date(call.message)

    if call.data.startswith(calendar_date_from.prefix):  # обработка кнопок от календаря calendar_date_from
        text_choice: str = 'Вы выбрали дату въезда:'
        calendar_call(
            call, calendar_date_from.sep, text_choice, markup_choice_date_from(), markup_choice_cancel(), 'check_in'
        )

    if call.data.startswith(calendar_date_before.prefix):  # обработка кнопок от календаря calendar_date_before
        text_choice: str = 'Вы выбрали дату выезда:'
        calendar_call(
            call, calendar_date_before.sep, text_choice, markup_choice_date_before(), markup_before_cancel(),
            'check_out'
        )

    if call.data == 'date_from_right':  # обработка кнопок от выбора даты въезда
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        set_state(call.message.chat.id, 'date_before')
        before_date(call.message)
    if call.data == 'date_from_to_change':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        from_date(call.message)
    if call.data == 'date_from_cancel':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        any_state(call.message)
    if call.data == 'date_from_to_continue':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        from_date(call.message)

    if call.data == 'date_before_right':  # обработка кнопок от выбора даты выезда
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        check_dates(call.message.chat.id)

    if call.data == 'date_before_to_change':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        before_date(call.message)
    if call.data == 'date_before_cancel':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        any_state(call.message)
    if call.data == 'date_before_to_continue':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        before_date(call.message)

    if call.data == "choice_photo_yes":  # обработка кнопок от выбора показа фото
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id, text="Вы выбрали 'Да'. Напишите количество фотографий для показа (1-10):"
        )
        set_state(call.message.chat.id, 'choice_photo_number')
    if call.data == "choice_photo_no":
        set_current_requests(call.message.chat.id, current_images=0)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text="Вы выбрали 'Нет'. Фотографии показывается не будут")
        set_state(call.message.chat.id, '0')
        if get_current_requests(call.message.chat.id, "command") == 'lowprice':
            request_hotels(call.message.chat.id, 'PRICE')
        elif get_current_requests(call.message.chat.id, "command") == 'highprice':
            request_hotels(call.message.chat.id, 'PRICE_HIGHEST_FIRST')
