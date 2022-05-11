import os
from typing import Tuple

from dotenv import find_dotenv, load_dotenv
from peewee import SqliteDatabase

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS: Tuple = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', "Узнать топ самых дешёвых отелей в городе"),
    ('highprice', "Узнать топ самых дорогих отелей в городе"),
    ('bestdeal', "Узнать топ отелей, наиболее подходящих по цене и расположению от центра"),
    ('history', "Узнать историю поиска отелей."),
    ('cancel', "Завершить команду")
)
DATABASE: str = 'users.db'
USER_DATABASE: SqliteDatabase = SqliteDatabase(DATABASE)

DATA_HISTORY: str = 'history.pickle'
NUMBER_HISTORY: int = 5
