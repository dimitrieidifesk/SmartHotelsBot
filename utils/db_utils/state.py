from typing import Union

from config_data.config import USER_DATABASE
from database.pewee_database import UserStates


def get_state(current_id: int, column: str) -> Union[str, int]:
    """
    Функция возвращает значение состояния пользователя из таблицы UserStates users_database.
    """
    query = UserStates.select().where(UserStates.chat_id == current_id)
    if query.exists():
        row = UserStates.get(UserStates.chat_id == current_id)
        USER_DATABASE.close()
        if column == 'states':
            return row.states
        elif column == 'message_id':
            return row.message_id
    else:
        USER_DATABASE.close()
        return '0'


def set_state(current_id: int, states: str = None, message_id: int = None) -> None:
    """
    Функция устанавливает состояние пользователя в таблицу UserStates users_database.
    """
    query = UserStates.select().where(UserStates.chat_id == current_id)
    if not query.exists():
        UserStates.create(chat_id=current_id, states='0', message_id=0)

    row = UserStates.get(UserStates.chat_id == current_id)
    if states:
        row.states = states
    if message_id:
        row.message_id = message_id
    row.save()
    USER_DATABASE.close()
