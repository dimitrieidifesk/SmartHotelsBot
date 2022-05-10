from loguru import logger
from telebot.types import Message

from loader import bot
from utils.db_utils.current_requests import set_current_requests
from utils.db_utils.state import get_state, set_state


@bot.message_handler(func=lambda message: 'distance_min' == get_state(message.chat.id, 'states'))
@logger.catch
def min_distance_choice(message: Message) -> None:
    """Функция - хэндлер получает от пользователя минимальное расстояние до центра.
    """
    chat_id: int = message.chat.id
    if message.text.isdigit():
        distance: int = int(message.text)
        if distance >= 0:
            set_current_requests(chat_id, distance_min=distance)
            set_state(chat_id, states='distance_max')
            bot.send_message(
                chat_id, "Введите желаемое максимальное расстояние до центра города (целое число, километры):"
            )
        else:
            bot.send_message(chat_id, 'Ошибка, введите число больше или равно 0.')
    else:
        bot.send_message(chat_id, 'Ошибка, введите число больше или равно 0.')
