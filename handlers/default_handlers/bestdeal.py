from loguru import logger
from telebot.types import Message

from loader import bot
from utils.db_utils.current_requests import set_current_requests
from utils.db_utils.state import set_state


@bot.message_handler(commands=['bestdeal'])
@logger.catch
def send_bestdeal(message: Message) -> None:
    """
    Функция-хэндлер предлагает ввести город для поиска bestdeal.
    """
    chat_id: int = message.chat.id
    logger.info(f"В чате - {chat_id} пользователь запустил команду bestdeal")
    set_state(chat_id, states='city')
    set_current_requests(chat_id, default=True)
    set_current_requests(chat_id, current_command='bestdeal')
    bot.send_message(
        chat_id, 'Вы выбрали - узнать топ отелей, наиболее подходящих по цене и расположению от центра.\n'
        'В каком городе ищем?'
    )
