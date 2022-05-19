import logging
from datetime import datetime, timedelta, timezone, date

from source import settings


def set_logger():
    logging.basicConfig(level=logging.INFO)


def get_date_time_from_timestamp_with_offset(timestamp_in_milliseconds, offset_in_milliseconds):
    tz = timezone(timedelta(seconds=offset_in_milliseconds / 1000))
    return datetime.fromtimestamp(timestamp_in_milliseconds / 1000, tz)


def get_datetime_from_string(date_string):
    return datetime.strptime(date_string, settings.DATE_FORMAT)


def get_date_date_string_from_date(a_date):
    return date.strftime(a_date, settings.DATE_FORMAT)
