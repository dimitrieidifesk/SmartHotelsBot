from loguru import logger
from telebot.types import CallbackQuery, Message

from handlers.default_handlers.bestdeal import send_bestdeal
from handlers.default_handlers.high_price import send_highprice
from handlers.default_handlers.history import send_history
from handlers.default_handlers.low_price import send_lowprice
from loader import bot


@logger.catch
def commands_call(call: CallbackQuery) -> None:
    """
    Функция обрабатывает нажатия кнопок от выбора команд
    """
    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id
    message: Message = call.message
    bot.edit_message_reply_markup(chat_id, message_id)
    # TODO можно заменить на if elif else ? часть условий

    if call_data == "lowprice":
        bot.send_message(call.message.chat.id, f"Вы выбрали /{call_data}")
        send_lowprice(message)
    if call_data == "highprice":
        bot.send_message(chat_id, f"Вы выбрали /{call_data}")
        send_highprice(message)
    if call_data == "bestdeal":
        bot.send_message(chat_id, f"Вы выбрали /{call_data}")
        send_bestdeal(message)
    if call_data == "history":
        bot.send_message(chat_id, f"Вы выбрали /{call_data}")
        send_history(message)
