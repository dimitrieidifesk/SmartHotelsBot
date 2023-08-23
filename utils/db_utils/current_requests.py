from typing import Union

from config_data.config import USER_DATABASE
from database.pewee_database import CurrentRequests


def get_current_requests(current_id: int, column: str) -> Union[str, int]:
    """
    Функция возвращает значения колонок из таблицы CurrentRequests users_database.
    """
    query = CurrentRequests.select().where(CurrentRequests.chat_id == current_id)
    if query.exists():
        row = CurrentRequests.get(CurrentRequests.chat_id == current_id)
        if column == "command":
            USER_DATABASE.close()
            return row.command
        elif column == "destination_id":
            USER_DATABASE.close()
            return row.destination_id
        elif column == "hotels":
            USER_DATABASE.close()
            return row.hotels
        elif column == "images":
            USER_DATABASE.close()
            return row.images
        elif column == "check_in":
            USER_DATABASE.close()
            return row.check_in
        elif column == "check_out":
            USER_DATABASE.close()
            return row.check_out
        elif column == "distance_min":
            USER_DATABASE.close()
            return row.distance_min
        elif column == "distance_max":
            USER_DATABASE.close()
            return row.distance_max
        elif column == "price_min":
            USER_DATABASE.close()
            return row.price_min
        elif column == "price_max":
            USER_DATABASE.close()
            return row.price_max
    else:
        USER_DATABASE.close()
        return "0"


def set_current_requests(
    current_id: int,
    default: bool = False,
    current_command: str = None,
    current_destination_id: int = None,
    current_hotels: int = None,
    current_images: int = None,
    current_check_in: str = None,
    current_check_out: str = None,
    price_min: int = None,
    price_max: int = None,
    distance_min: int = None,
    distance_max: int = None,
) -> None:
    """
    Функция с переданным параметром default=True устанавливает
    в таблице CurrentRequests users_database дефолтные значения.
    Без default записывает в колонки таблицы переданные значения.
    """
    if default:
        query = CurrentRequests.select().where(CurrentRequests.chat_id == current_id)
        if query.exists():
            row = CurrentRequests.delete().where(CurrentRequests.chat_id == current_id)
            row.execute()
            USER_DATABASE.close()
            return
        else:
            USER_DATABASE.close()
            return
    query = CurrentRequests.select().where(CurrentRequests.chat_id == current_id)
    if not query.exists():
        CurrentRequests.create(
            chat_id=current_id,
            command="0",
            destination_id=0,
            hotels=0,
            images=0,
            check_in="0",
            check_out="0",
            price_min=0,
            price_max=0,
            distance_min=0,
            distance_max=0,
        )
    row = CurrentRequests.get(CurrentRequests.chat_id == current_id)
    if current_command:
        row.command = current_command
    if current_destination_id:
        row.destination_id = current_destination_id
    if current_hotels:
        row.hotels = current_hotels
    if current_images:
        row.images = current_images
    if current_check_in:
        row.check_in = current_check_in
    if current_check_out:
        row.check_out = current_check_out
    if price_min:
        row.price_min = price_min
    if price_max:
        row.price_max = price_max
    if distance_min:
        row.distance_min = distance_min
    if distance_max:
        row.distance_max = distance_max
    row.save()
    USER_DATABASE.close()
