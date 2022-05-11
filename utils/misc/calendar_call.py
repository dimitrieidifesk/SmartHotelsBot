from loguru import logger

from keyboards.other.calendar import calendar
from loader import bot
from utils.db_utils.current_requests import set_current_requests


@logger.catch
def calendar_call(call, sep, text_choice: str, markup_day, markup_cancel, edit_column: str) -> None:
    """
    Функция обрабатывает call календаря
    """
    chat_id: int = call.message.chat.id
    name, action, year, month, day = call.data.split(sep)
    date_choice = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    if action == "DAY":
        bot.send_message(chat_id, f"{text_choice} {date_choice.strftime('%Y-%m-%d')}", reply_markup=markup_day)
        result: str = date_choice.strftime('%Y-%m-%d')
        if edit_column == 'check_in':
            set_current_requests(chat_id, current_check_in=result)
        elif edit_column == 'check_out':
            set_current_requests(chat_id, current_check_out=result)
    elif action == "CANCEL":
        bot.send_message(chat_id, "Хотите завершить?", reply_markup=markup_cancel)
