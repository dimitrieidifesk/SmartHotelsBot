from typing import Dict, List

import telebot
from loguru import logger
from telebot.types import Message, InlineKeyboardMarkup
from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton

from keyboards.reply.history_markup import show_commands
from loader import bot
from utils.db_utils.database_history import get_pickle
from utils.db_utils.pagination import get_pagination, set_pagination
from utils.db_utils.state import set_state, get_state


@bot.message_handler(commands=['history'])
@logger.catch
def send_history(message: Message) -> None:
    """
    Функция-хэндлер отправляет пользователю историю запросов.
    """
    chat_id: int = message.chat.id
    logger.info(f"В чате - {chat_id} пользователь запустил команду history")
    date: Dict = get_pickle(chat_id)
    if not date:
        bot.send_message(chat_id, "История поиска пуста.")

    else:
        markup: InlineKeyboardMarkup = show_commands(list(date.keys()))
        bot.send_message(chat_id, "Выберите историю поиска которую показать:", reply_markup=markup)
        set_state(chat_id, states="choice_history")


@logger.catch
def send_character_page(message, page=1, command=None, city_id=None):
    """
    Функция предоставляет историю отелей пагинацией.
    """
    chat_id: int = message.chat.id
    if command:
        date: Dict = get_pickle(chat_id)
        hotels_pages: List = date[command][city_id][1:]
    else:
        command_pickle, city_id_pickle = get_pagination(message.id)
        date: Dict = get_pickle(chat_id)
        hotels_pages: List = date[command_pickle][city_id_pickle][1:]

    paginator: InlineKeyboardPaginator = InlineKeyboardPaginator(
        len(hotels_pages),
        current_page=page,
        data_pattern='character#{page}'
    )
    paginator.add_after(InlineKeyboardButton('Закрыть', callback_data='back'))
    if command:
        current_message: Message = bot.send_message(
            chat_id,
            hotels_pages[page - 1],
            reply_markup=paginator.markup,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        set_pagination(current_message.id, city_id, command)
        set_state(chat_id, message_id=current_message.id)
    else:
        message_id: int = get_state(chat_id, "message_id")
        try:
            bot.edit_message_text(
                chat_id=message.chat.id, message_id=message_id,
                text=hotels_pages[page - 1],
                reply_markup=paginator.markup,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        except telebot.apihelper.ApiTelegramException:
            pass
