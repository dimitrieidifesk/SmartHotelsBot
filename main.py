import time

from loguru import logger
from telebot import custom_filters

from config_data.config import USER_DATABASE
from database.pewee_database import UserStates, Cities, CurrentRequests, HotelsPagination
from loader import bot
from utils.db_utils.database_history import create_pickle
from utils.set_bot_commands import set_default_commands
import handlers


@logger.catch
def main() -> None:
    """
    Функция запускает бота
    """
    logger.add(
        'logs/logs.log',
        level='DEBUG',
        format="{time} {level} {message}",
        rotation='1 week',
        retention='1 week',
        compression='zip'
    )
    set_default_commands(bot)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    USER_DATABASE.create_tables([UserStates, Cities, CurrentRequests, HotelsPagination])
    USER_DATABASE.close()
    create_pickle()

    while True:
        try:
            logger.info("Запуск бота")
            bot.polling(skip_pending=True)
        except KeyboardInterrupt:
            exit('Завершение программы')
        except Exception as error:
            logger.info(f"Ошибка - {error}")
            bot.stop_polling()
            time.sleep(1)


if __name__ == '__main__':
    main()
