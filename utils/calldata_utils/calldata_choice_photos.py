import telebot
from loguru import logger
from telebot.types import CallbackQuery

from utils.db_utils.current_requests import set_current_requests, get_current_requests
from utils.db_utils.state import set_state
from utils.misc.hotels_requests import request_hotels
from loader import bot
from utils.misc.request_hotels_bestdeal import request_hotels_bestdeal


@logger.catch
def calldata_choice_photos(call: CallbackQuery) -> None:
    """
    Функция обрабатывает кнопки выбора показа фото
    """
    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id
    try:
        bot.edit_message_reply_markup(chat_id, message_id)
    except telebot.apihelper.ApiTelegramException as error:
        logger.info(f"Ошибка - {error}")

    if call_data == "choice_photo_yes":
        bot.send_message(chat_id, "Вы выбрали 'Да'. Напишите количество фотографий для показа (1-10):")
        set_state(chat_id, states='choice_photo_number')
    if call_data == "choice_photo_no":
        bot.send_message(chat_id, "Вы выбрали 'Нет'. Фотографии показывается не будут")
        set_current_requests(chat_id, current_images=0)
        set_state(chat_id, states='send_result')
        command = get_current_requests(chat_id, "command")
        if command == 'lowprice':
            request_hotels(chat_id, 'PRICE')
        elif command == 'highprice':
            request_hotels(chat_id, 'PRICE_HIGHEST_FIRST')
        elif command == 'bestdeal':
            request_hotels_bestdeal(chat_id)
