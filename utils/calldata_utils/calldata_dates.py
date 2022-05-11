from loguru import logger
from telebot.types import CallbackQuery, Message

from handlers.default_handlers.before_date import before_date
from handlers.default_handlers.cancel import any_state
from utils.db_utils.state import set_state
from utils.misc.check_dates import check_dates
from handlers.default_handlers.from_date import from_date
from loader import bot


@logger.catch
def calldata_dates(call: CallbackQuery) -> None:
    """
    Функция обрабатывает кнопок от выбора даты въезда и выезда
    """
    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id
    message: Message = call.message
    bot.edit_message_reply_markup(chat_id, message_id)

    # TODO можно заменить на if elif else ? часть условий
    if call_data == 'date_from_right':
        set_state(chat_id, states='date_before')
        before_date(message)
    if call_data == 'date_from_to_change':
        from_date(message)
    if call_data == 'date_from_cancel':
        any_state(message)
    if call_data == 'date_from_to_continue':
        from_date(message)

    if call_data == 'date_before_right':
        check_dates(chat_id)
    if call_data == 'date_before_to_change':
        before_date(message)
    if call_data == 'date_before_cancel':
        any_state(message)
    if call_data == 'date_before_to_continue':
        before_date(message)
