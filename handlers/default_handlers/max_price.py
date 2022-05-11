from loguru import logger
from telebot.types import Message

from loader import bot
from utils.db_utils.current_requests import get_current_requests, set_current_requests
from utils.db_utils.state import get_state, set_state


@bot.message_handler(func=lambda message: 'price_max' == get_state(message.chat.id, 'states'))
@logger.catch
def max_price_choice(message: Message) -> None:
    """Функция - хэндлер получает от пользователя максимальную стоимость отеля.
    """
    chat_id: int = message.chat.id
    if message.text.isdigit():
        price = int(message.text)
        min_price: int = get_current_requests(chat_id, 'price_min')
        if price >= 0:
            if price - min_price > 0:
                set_current_requests(chat_id, price_max=price)
                set_state(chat_id, states='distance_min')
                bot.send_message(chat_id, f"Выбранный диапазон цен {min_price} - {price} рублей")
                bot.send_message(
                    chat_id, "Введите желаемое минимальное расстояние до центра города (целое число, километры):"
                )
            else:
                bot.send_message(chat_id, f'Ошибка, введите число больше, чем минимальное - {min_price}.')
        else:
            bot.send_message(chat_id, 'Ошибка, введите число больше или равно 0.')

    else:
        bot.send_message(chat_id, 'Ошибка, введите число больше или равно 0.')
