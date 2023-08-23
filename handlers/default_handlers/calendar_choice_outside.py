from loader import bot
from loguru import logger
from telebot.types import Message
from utils.db_utils.state import get_state


@bot.message_handler(func=lambda message: "calendar_choice" in get_state(message.chat.id, "states"))
@logger.catch
def outside_algorithm(message: Message) -> None:
    """Функция перехватывает сообщения при выборе с клавиатуры."""
    bot.send_message(message.chat.id, "Воспользуйтесь предложенным выбором.")
