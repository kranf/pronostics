from datetime import timedelta

from source.utils import get_datetime_from_string


def get_iterator(start_date, end_date):
    """takes start and end date argument as string in with the default format or directly as date"""
    _start_date = get_datetime_from_string(start_date) if isinstance(start_date, str) else start_date
    _end_date = get_datetime_from_string(end_date) if isinstance(end_date, str) else end_date
    return DateIterable(_start_date, _end_date)

class DateIterable:

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        return self

    def __next__(self):
        if self._present_day > self.end_date:
            raise StopIteration
        today = self._present_day
        self._present_day += timedelta(days=1)
        return today
