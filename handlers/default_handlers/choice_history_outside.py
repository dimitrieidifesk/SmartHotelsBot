from loguru import logger
from telebot.types import Message

from loader import bot
from utils.db_utils.state import get_state


@bot.message_handler(func=lambda message: 'choice_history' in get_state(message.chat.id, 'states'))
@logger.catch
def send_choice_history(message: Message) -> None:
    """Функция перехватывает сообщения при работе пользователя с историей.
    """
    bot.send_message(message.chat.id, 'Воспользуйтесь предложенным выбором.')
