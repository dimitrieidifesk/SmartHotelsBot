from loguru import logger
from telebot.types import Message

from database.utils_db import set_state, set_current_requests
from loader import bot


@bot.message_handler(commands=['highprice'])
@logger.catch
def send_highprice(message: Message) -> None:
    """
    Функция-хэндлер предлагает ввести город для поиска.
    """
    if message.from_user.full_name != "HotelsFindBot":
        logger.info(
            f"Пользователь {message.from_user.full_name}({message.from_user.username}),"
            f" message.chat.id - {message.chat.id} запустил команду highprice"
        )
    else:
        logger.info(
            f"Бот из чата - {message.chat.id} запустил команду highprice"
        )
    set_state(current_id=message.chat.id, user_states='city')
    set_current_requests(message.chat.id, default=True)
    set_current_requests(message.chat.id, current_command='highprice')
    bot.send_message(message.chat.id, 'Вы выбрали - узнать топ самых дорогих отелей в городе.\nВ каком городе ищем?')
