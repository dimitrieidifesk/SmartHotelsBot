from loguru import logger
from telebot.types import Message

from loader import bot
from utils.db_utils.state import get_state


@bot.message_handler(func=lambda message: 'choice_cities' in get_state(message.chat.id, 'states'))
@logger.catch
def send_city_outside(message: Message):
    """
    Функция обрабатывает сообщения состояния choice_cities.
    """
    bot.send_message(message.chat.id, 'Пожалуйста выберите город из списка выше')
