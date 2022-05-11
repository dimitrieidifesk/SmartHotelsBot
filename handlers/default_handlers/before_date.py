from datetime import datetime

from loguru import logger
from telebot.types import Message

from keyboards.other.calendar import calendar, calendar_date_before
from loader import bot
from utils.db_utils.state import get_state, set_state


@bot.message_handler(func=lambda message: 'date_before' in get_state(message.chat.id, 'states'))
@logger.catch
def before_date(message: Message) -> None:
    """
    Функция-хэндлер предлагает пользователю выбор дату выезда.
    """
    chat_id: int = message.chat.id
    now: datetime = datetime.now()
    bot.send_message(
        chat_id,
        "Выберите дату выезда из гостиницы",
        reply_markup=calendar.create_calendar(
            name=calendar_date_before.prefix,
            year=now.year,
            month=now.month,
        ),
    )
    set_state(chat_id, states='calendar_choice')
