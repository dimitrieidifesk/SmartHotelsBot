from loguru import logger
from telebot.types import Message

from handlers.default_handlers.start import bot_start
from loader import bot


@logger.catch
@bot.message_handler(content_types="text")
def bot_echo(message: Message) -> None:
    """
    Функция хендлер, перехватывает текстовые сообщения без указанного состояния.
    """
    if message.text.lower() in ('ghbdtn', 'привет'):
        bot_start(message)
    else:
        bot.reply_to(message, "Я тебя не понимаю. Напиши /help.")


@logger.catch
@bot.message_handler(
    content_types=[
        "audio", "document", "photo", "sticker", "video",
        "video_note", "video_note", "voice", "location", "contact"
    ]
)
def message_reply(message: Message) -> None:
    """
    Функция отвечает на отличные от текстовых сообщения пользователя.
    """
    bot.reply_to(message, "Я тебя не понимаю. Напиши /help.")
