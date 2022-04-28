from source.dao import RaceDao
from source.data_service import DataService


def get_data_service(db_uri):
    raceDao = RaceDao(db_uri)
    return DataService(raceDao)