from loguru import logger

from loader import bot
from utils.db_utils.current_requests import set_current_requests
from utils.db_utils.state import set_state


@bot.message_handler(commands=['cancel'])
@logger.catch
def any_state(message):
    """
    Функция сбрасывает состояния пользователя
    """
    chat_id: int = message.chat.id
    bot.send_message(chat_id, "Ваша команда отменена, чтобы начать заново введите /start")
    set_state(chat_id, states='0')
    set_current_requests(chat_id, default=True)
