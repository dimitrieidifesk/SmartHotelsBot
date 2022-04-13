from loguru import logger

from database.utils_db import set_state, set_current_requests
from loader import bot


@bot.message_handler(commands=['cancel'])
@logger.catch
def any_state(message):
    """
    Функция сбрасывает состояния пользователя
    """
    bot.send_message(message.chat.id, "Ваша команда отменена, чтобы начать заново введите /start")
    set_state(message.chat.id, '0')
    set_current_requests(message.chat.id, default=True)
