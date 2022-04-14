from typing import List

from loguru import logger
from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from database.utils_db import set_state
from loader import bot


@bot.message_handler(commands=['help'])
@logger.catch
def bot_help(message: Message) -> None:
    """
    Функция хэндлер отвечает на команду help
    """
    text: List = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    text.append("Напиши /start либо 'привет', чтобы начать")
    bot.reply_to(message, '\n'.join(text))
    set_state(message.chat.id, '0')
