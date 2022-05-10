from loguru import logger
from telebot.types import Message

from loader import bot
from utils.db_utils.current_requests import set_current_requests
from utils.db_utils.state import get_state, set_state


@bot.message_handler(func=lambda message: 'price_min' == get_state(message.chat.id, 'states'))
@logger.catch
def min_price_choice(message: Message) -> None:
    """Функция - хэндлер получает от пользователя минимальную стоимость отеля.
    """
    chat_id: int = message.chat.id
    if message.text.isdigit():
        price = int(message.text)
        if price >= 0:
            set_current_requests(chat_id, price_min=price)
            set_state(chat_id, states='price_max')
            bot.send_message(chat_id, "Введите желаемую максимальную стоимость за ночь в рублях (целое число):")
        else:
            bot.send_message(chat_id, 'Ошибка, введите число больше или равно 0.')
    else:
        bot.send_message(chat_id, 'Ошибка, введите число больше или равно 0.')
