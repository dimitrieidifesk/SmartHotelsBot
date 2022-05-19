import telebot
from loguru import logger
from telebot.types import CallbackQuery

from handlers.default_handlers.cancel import any_state
from handlers.default_handlers.low_price import send_lowprice
from loader import bot


@logger.catch
def cities_call(call: CallbackQuery) -> None:
    """
    Функция обрабатывает нажатия на кнопки выбора города
    """
    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id
    try:
        bot.edit_message_reply_markup(chat_id, message_id)
    except telebot.apihelper.ApiTelegramException as error:
        logger.info(f"Ошибка - {error}")

    if call_data == "city_yes":
        bot.send_message(chat_id, "Вы выбрали 'Да'")
        send_lowprice(call.message)
    if call_data == "city_no":
        bot.send_message(chat_id, "Вы выбрали 'Нет'")
        any_state(call.message)
