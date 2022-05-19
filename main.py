import time

from loguru import logger

from config_data.config import USER_DATABASE
from database.pewee_database import UserStates, Cities, CurrentRequests, HotelsPagination
from loader import bot
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
    USER_DATABASE.create_tables([UserStates, Cities, CurrentRequests, HotelsPagination])
    USER_DATABASE.close()

    while True:
        try:
            logger.info("Запуск бота")
            bot.polling(skip_pending=True)
        except KeyboardInterrupt:
            logger.info("Завершение работы")
            exit()
            return
        except Exception as error:
            logger.info(f"Ошибка - {error}")
            bot.stop_polling()
            time.sleep(1)


if __name__ == '__main__':
    main()
