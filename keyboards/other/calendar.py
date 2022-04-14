from typing import Any

from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

calendar: Any = Calendar(language=RUSSIAN_LANGUAGE)
calendar_date_from: Any = CallbackData("calendar_date_from", "action", "year", "month", "day")
calendar_date_before: Any = CallbackData("calendar_date_before", "action", "year", "month", "day")
