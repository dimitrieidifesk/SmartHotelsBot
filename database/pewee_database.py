from peewee import Model, TextField, IntegerField

from config_data.config import users_database


class Cities(Model):
    """
    Класс Cities используется для создания таблицы хранящих сведения о найденных городах в БД users_database
    Attributes
    _________
    destination_id: int = ИД города
    name: str = название города
    latitude: str =  широта
    longitude: str = долгота
    """
    destination_id = IntegerField(primary_key=True)
    name = TextField()
    latitude = TextField()
    longitude = TextField()

    class Meta:
        database = users_database


class CurrentRequests(Model):
    """
    Класс CurrentRequests используется для создания таблицы хранящей сведения о текущем запросе в БД users_database
    Attributes
    _________
    chat_id: int = ИД чата
    command: str = команда пользователя
    destination_id: int =  ИД города
    hotels: int = количество отелей для показа
    images: int = количество фотографий
    check_in: str =  дата въезда
    check_out: str =  дата выезда
    """
    chat_id = IntegerField(primary_key=True)
    command = TextField()
    destination_id = IntegerField()
    hotels = IntegerField()
    images = IntegerField()
    check_in = TextField()
    check_out = TextField()

    class Meta:
        database = users_database


class UserStates(Model):
    """
    Класс UserStates используется для создания таблицы хранящих сведения о состоянии пользователя в БД users_database
    Attributes
    _________
    chat_id: int = ИД чата
    states: str = состояние пользователя
    """
    chat_id = IntegerField(primary_key=True)
    states = TextField()

    class Meta:
        database = users_database
