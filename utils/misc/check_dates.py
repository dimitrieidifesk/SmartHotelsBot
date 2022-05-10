from datetime import date, datetime, timedelta
from typing import Union

from loguru import logger
from loader import bot
from utils.db_utils.current_requests import get_current_requests, set_current_requests
from utils.db_utils.state import set_state
from utils.misc.check_date import check_date, get_date


@logger.catch
def check_dates(chat_id: int) -> None:
    """
    Функция проверяет введенные пользователем даты.
    """
    bot.send_message(chat_id, 'Проверяю даты...')
    check: bool = True
    date_in: Union[str, date] = get_current_requests(chat_id, "check_in")
    date_out: str = get_current_requests(chat_id, "check_out")
    date_today: str = datetime.today().strftime('%Y-%m-%d')

    if check_date(date_today, date_in) < 0:
        bot.send_message(chat_id, f'Дата въезда установлена на сегодня: {date_today}')
        set_current_requests(chat_id, current_check_in=date_today)
        check: bool = False
    date_in = get_current_requests(chat_id, "check_in")
    if check_date(date_in, date_out) <= 0:
        date_in = get_date(date_in)
        date_in = date_in + timedelta(days=1)
        date_in = date_in.strftime('%Y-%m-%d')
        bot.send_message(chat_id, f'Дата выезда установлена на следующий день: {date_in}')
        set_current_requests(chat_id, current_check_out=date_in)
        check = False
    if check:
        bot.send_message(chat_id, 'Все ок.')
    bot.send_message(chat_id, 'Напишите количество отелей для показа (1-25):')
    set_state(chat_id, states='hotels_number')
