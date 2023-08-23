from loguru import logger
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


@logger.catch
def set_default_commands(bot) -> None:
    """
    Функция устанавливает команды бота по умолчанию
    """
    bot.set_my_commands([BotCommand(*command) for command in DEFAULT_COMMANDS])
