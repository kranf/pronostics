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


def get_date_string_from_date(a_date):
    return date.strftime(a_date, settings.DATE_FORMAT)

def convert_horse_distance(distance):
    """

    Nez : 0,05L
    Courte tête : 0,08L
    Tête : 0,1L
    Courte encolure : 0,15L
    Encolure : 0,25L
    ½ longueur : 0,5L
    ¾ longueur : 0,75L
    1 longueur : 1L
    1 ½ longueurs : 1,5L
    2 longueurs : 2L
    3 longueurs : 3L

    1L = 2.4m
    """
    length_unit_in_meter = 2.4

    distance_dict = {
        "nez": 0.05,
        "cte tete": 0.08,
        "tete": 0.1,
        "cte enc.": 0.15,
        "encolure": 0.25,
    }

    fraction_dict = {
        "1/4": 0.25,
        "1/2": 0.5,
        "3/4": 0.75,
    }

    standard_unit = 'L'

    if not standard_unit in distance:
        if not distance.lower() in distance_dict:
            raise RuntimeError(f'Unknown distance {distance}')
        return distance_dict[distance.lower()] * length_unit_in_meter

    before_unit, after_unit = distance.split(standard_unit)

    distance_as_number = fraction_dict[before_unit.strip()] if '/' in before_unit else int(before_unit.strip())
    distance_as_number = distance_as_number if not after_unit else distance_as_number + fraction_dict[after_unit.strip()]
    return distance_as_number * length_unit_in_meter