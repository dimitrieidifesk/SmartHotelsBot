from loguru import logger
from telebot.types import CallbackQuery

from config_data.config import DEFAULT_COMMANDS
from handlers.default_handlers.history import send_history
from keyboards.reply.common_markup import markup_start
from keyboards.reply.history_markup import show_search_hotel
from loader import bot
from utils.db_utils.state import set_state


@logger.catch
def calldata_choice_history(call: CallbackQuery) -> None:
    """
    Функция обрабатывает кнопки от выбора показа истории команд
    """
    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id

    if call_data == "ecirpwol":
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id,
            text="Вы выбрали историю 'lowprice'.\nВыберите один из вариантов ниже:",
            reply_markup=show_search_hotel(call_data[::-1], chat_id))
    elif call_data == "ecirphgih":
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id,
            text="Вы выбрали историю 'highprice'.\nВыберите один из вариантов ниже:",
            reply_markup=show_search_hotel(call_data[::-1], chat_id))
    elif call_data == "laedtseb":
        bot.edit_message_text(
            chat_id=chat_id, message_id=message_id,
            text="Вы выбрали историю 'bestdeal'.\nВыберите один из вариантов ниже:",
            reply_markup=show_search_hotel(call_data[::-1], chat_id))
    elif call_data == "close_history":
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_message(
            chat_id, "История закрыта, желаете продолжить?\n"
            "Выберите команду:", reply_markup=markup_start(DEFAULT_COMMANDS)
        )
        bot.send_message(chat_id, "Описание команд - /help")
        set_state(chat_id, states='0')
    else:
        # "close_hotels"
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        send_history(call.message)
