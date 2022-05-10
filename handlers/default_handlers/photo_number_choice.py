from loguru import logger
from telebot.types import Message

from utils.db_utils.current_requests import get_current_requests, set_current_requests
from utils.db_utils.state import get_state, set_state
from utils.misc.hotels_requests import request_hotels
from loader import bot
from utils.misc.request_hotels_bestdeal import request_hotels_bestdeal


@bot.message_handler(func=lambda message: 'choice_photo_number' in get_state(message.chat.id, 'states'))
@logger.catch
def choice_photo_number(message: Message) -> None:
    """
        Функция-хэндлер устанавливает количество показываемых фотографий.
    """
    chat_id: int = message.chat.id
    command = get_current_requests(chat_id, "command")
    set_state(chat_id, states='send_result')
    if message.text.isdigit():
        number: int = int(message.text)
        if number > 10 or number < 1:
            bot.send_message(chat_id, 'Некорректный ввод.\nБудут показаны не более 10 фотографий')
            set_current_requests(chat_id, current_images=10)
            if command == 'lowprice':
                request_hotels(chat_id, 'PRICE')
            elif command == 'highprice':
                request_hotels(chat_id, 'PRICE_HIGHEST_FIRST')
            elif command == 'bestdeal':
                request_hotels_bestdeal(chat_id)
        else:
            bot.send_message(chat_id, f'Будут показаны {number} фотографий')
            set_current_requests(chat_id, current_images=number)
            if command == 'lowprice':
                request_hotels(chat_id, 'PRICE')
            elif command == 'highprice':
                request_hotels(chat_id, 'PRICE_HIGHEST_FIRST')
            elif command == 'bestdeal':
                request_hotels_bestdeal(chat_id)

    else:
        bot.send_message(chat_id, 'Некорректный ввод.\nБудут показаны не более 10 фотографий')
        set_current_requests(chat_id, current_images=10)
        if command == 'lowprice':
            request_hotels(chat_id, 'PRICE')
        elif command == 'highprice':
            request_hotels(chat_id, 'PRICE_HIGHEST_FIRST')
        elif command == 'bestdeal':
            request_hotels_bestdeal(chat_id)
