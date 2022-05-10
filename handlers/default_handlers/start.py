from loguru import logger
from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from keyboards.reply.common_markup import markup_start
from loader import bot
from utils.db_utils.state import set_state


@bot.message_handler(commands=['start'])
@logger.catch
def bot_start(message: Message):
    bot.reply_to(
        message, "Привет я бот, помогу тебе выбрать отель в нужном городе!\n"
                 "Выберите команду:", reply_markup=markup_start(DEFAULT_COMMANDS)
    )
    bot.send_message(message.from_user.id, "Описание команд - /help")
    set_state(message.chat.id, states='0')
