from loguru import logger
from telebot import custom_filters

from config_data.config import users_database
from database.pewee_database import UserStates, Cities, CurrentRequests
from loader import bot
from utils.set_bot_commands import set_default_commands
import handlers

if __name__ == '__main__':
    logger.add(
        'logs/logs.log',
        level='DEBUG',
        format="{time} {level} {message}",
        rotation='1 week',
        retention='1 week',
        compression='zip'
    )
    logger.info("Запуск бота")

    set_default_commands(bot)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    users_database.create_tables([UserStates, Cities, CurrentRequests])
    users_database.close()

    try:
        bot.infinity_polling(skip_pending=True)
    except KeyboardInterrupt:
        logger.info("Завершение работы бота")
        exit()
