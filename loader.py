from config_data import config
from telebot import TeleBot

bot: TeleBot = TeleBot(token=config.BOT_TOKEN)
