from keyboards.reply.common_markup import markup_choice_photo
from loader import bot
from loguru import logger
from telebot.types import Message
from utils.db_utils.current_requests import set_current_requests
from utils.db_utils.state import get_state, set_state


@bot.message_handler(func=lambda message: "hotels_number" in get_state(message.chat.id, "states"))
@logger.catch
def hotels_number_choice(message: Message) -> None:
    """
    Функция-хэндлер устанавливает количество показываемых отелей.
    """
    chat_id: int = message.chat.id
    if message.text.isdigit():
        number: int = int(message.text)
        if number > 25 or number < 1:
            bot.send_message(chat_id, "Некорректный ввод.\nБудут показаны не более 25 отелей")
            set_current_requests(chat_id, current_hotels=10)
        else:
            bot.send_message(chat_id, f"Будут показаны {number} отелей")
            set_current_requests(chat_id, current_hotels=number)
    else:
        bot.send_message(chat_id, "Некорректный ввод.\nБудут показаны не более 25 отелей")
        set_current_requests(chat_id, current_hotels=10)

    current_id_message = bot.send_message(
        chat_id, "Показывать фотографии отелей?", reply_markup=markup_choice_photo()
    )
    set_state(chat_id, states="images_choice", message_id=current_id_message.id)
