from loguru import logger
from telebot.types import Message

from loader import bot
from utils.db_utils.current_requests import get_current_requests
from utils.db_utils.state import get_state, set_state
from utils.misc.hotels_requests import request_hotels
from utils.misc.request_hotels_bestdeal import request_hotels_bestdeal


@bot.message_handler(func=lambda message: 'images_choice' in get_state(message.chat.id, 'states'))
@logger.catch
def send_choice_photo_outside(message: Message):
    """
    Функция обрабатывает сообщения состояния images_choice.
    """
    chat_id: int = message.chat.id
    command: str = get_current_requests(chat_id, "command")
    message_id: int = get_state(chat_id, 'message_id')
    if message.text.lower() in ('да', 'lf'):
        bot.edit_message_reply_markup(chat_id, message_id)
        bot.send_message(chat_id, "Вы выбрали 'Да'. Напишите количество фотографий для показа (1-10):")
        set_state(chat_id, states='choice_photo_number')
    elif message.text.lower() in ('нет', 'ytn'):
        bot.send_message(chat_id, "Вы выбрали 'Нет'")
        bot.edit_message_reply_markup(chat_id, message_id)
        set_state(chat_id, states='send_result')
        if command == 'lowprice':
            request_hotels(chat_id, 'PRICE')
        elif command == 'highprice':
            request_hotels(chat_id, 'PRICE_HIGHEST_FIRST')
        elif command == 'bestdeal':
            request_hotels_bestdeal(chat_id)
    else:
        bot.send_message(chat_id, "Выберите или напишите Да/Нет")
