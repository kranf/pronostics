import logging
from datetime import datetime, timedelta, timezone

def set_logger():
    logging.basicConfig(level=logging.INFO)

def get_date_time_from_timestamp_with_offset(timestamp_in_milliseconds, offset_in_milliseconds):
    tz = timezone(timedelta(seconds=offset_in_milliseconds/1000))
    return datetime.fromtimestamp(timestamp_in_milliseconds/1000, tz)

