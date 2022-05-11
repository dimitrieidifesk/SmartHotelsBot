from loguru import logger
from telebot.types import Message

from handlers.default_handlers.from_date import from_date
from loader import bot
from utils.db_utils.current_requests import get_current_requests, set_current_requests
from utils.db_utils.state import get_state, set_state


@bot.message_handler(func=lambda message: 'distance_max' == get_state(message.chat.id, 'states'))
@logger.catch
def max_distance_choice(message: Message) -> None:
    """Функция - хэндлер получает от пользователя максимальное расстояние до центра.
    """
    chat_id: int = message.chat.id
    if message.text.isdigit():
        min_distance: int = get_current_requests(chat_id, 'distance_min')
        distance: int = int(message.text)
        if distance >= 0:
            if distance - min_distance > 0:
                set_current_requests(chat_id, distance_max=distance)
                set_state(chat_id, states='date_from')
                bot.send_message(chat_id, f"Выбранный диапазон расстояния {min_distance} - {distance} км.")
                from_date(message)
            else:
                bot.send_message(chat_id, f'Ошибка, введите число больше, чем минимальное - {min_distance}.')
        else:
            bot.send_message(chat_id, 'Ошибка, введите число больше или равно 0.')
    else:
        bot.send_message(chat_id, 'Ошибка, введите число больше или равно 0.')
