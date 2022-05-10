from loguru import logger
from telebot.types import Message

from handlers.default_handlers.cancel import any_state
from handlers.default_handlers.low_price import send_lowprice
from loader import bot
from utils.db_utils.state import get_state


@bot.message_handler(func=lambda message: 'choice_not_cities' == get_state(message.chat.id, 'states'))
@logger.catch
def send_not_city_outside(message: Message):
    """
    Функция обрабатывает сообщения состояния choice_not_cities.
    """
    chat_id: int = message.chat.id
    message_id: int = get_state(chat_id, 'message_id')
    if message.text.lower() in ('да', 'lf'):
        bot.send_message(chat_id, text="Вы выбрали 'Да'")
        bot.edit_message_reply_markup(chat_id, message_id)
        send_lowprice(message)
    elif message.text.lower() in ('нет', 'ytn'):
        bot.send_message(chat_id, "Вы выбрали 'Нет'")
        bot.edit_message_reply_markup(chat_id, message_id)
        any_state(message)
    else:
        bot.send_message(chat_id, "Выберите или напишите Да/Нет")
