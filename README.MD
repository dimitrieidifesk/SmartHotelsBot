# Поиск отелей в Telegram

Этот бот позволяет быстро подбирать отели прямо в мессенджере Telegram по различным критериям поиска. 


## Особенности

Данный бот позволяет:
* подбирать отели по самой низкой или высокой цене;
* подбирать отели по лучшему соотношению цена/расстояние от центра города;
* задавать диапазон цен.



## Requirements

* Python 3.7+
* [pyTelegramBotAPI](https://github.com/python-telegram-bot/python-telegram-bot) – Python Telegram Bot API
* [requests](https://github.com/psf/requests) - библиотека requests
* [peewee](http://docs.peewee-orm.com/en/latest/) - база данных поисковых параметров каждого пользователя
* [telebot-calendar](https://github.com/FlymeDllVa/Telebot-Calendar) - календарь для выбора checkin-checkout
* [python-telegram-bot-pagination](https://github.com/ksinn/python-telegram-bot-pagination) - для показа истории отелей
* [geopy](https://github.com/geopy/geopy) - для определения расстояния отеля до центра города
* [validator-collection](https://github.com/jirutka/validator-collection) - для определения валидности ссылок фотографий
* [python-dotenv](https://github.com/theskumar/python-dotenv) - для безопасности учетных данных
Вы можете установить все зависимости, выполнив следующую команду: `pip install -r requirements.txt`

## Логирование

В скрипте этого бота используется модуль [loguru](https://github.com/Delgan/loguru) для логирования.


## Команды бота

* `/start` - запуск бота, выполняется автоматически при подключении к боту.
* `/help` - список команд и их описание.
* `/reset` - для рестарта.
* `/lowprice` - узнать топ самых дешёвых отелей в городе.
* `/highprice` - узнать топ самых дорогих отелей в городе.
* `/bestdeal` - узнать топ отелей, наиболее подходящих по цене и расположению от центра.
* `/history` - узнать историю поиска отелей.

## Как работать с ботом 
В файле .env.template вписать `BOT_TOKEN = "Ваш токен для бота, полученный от @BotFather"`
и `RAPID_API_KEY = "Ваш ключ полученный от API по адресу rapidapi.com/apidojo/api/hotels4/"`
После переименовать файл в .env
Для запуска бота выполнить в терминале команду `python3 main.py`
Список всех команд, поддерживаемых ботом, можно посмотреть по команде `/help`

### Вывод результата

Введите название населенного пункта. Бот выполнит запрос к hotels api выведет список отелей с указанием названия, 
класса, цены, адреса и расстояния от центра.
Пример результата:

![](img.png "Отель")

Если бот не найдет ни одну локацию, то уведомляет, что ничего не найдено и предложит повторить.


