import argparse
from datetime import datetime, date, timedelta

from dotenv import load_dotenv

from source import settings
from source.dao import RaceDao, create_session
from source.data_scrapping import get_mongo_data_service
from source.date_iterator import get_iterator
from source.model import Race
from source.utils import set_logger, get_date_string_from_date
import logging
import os

set_logger()

load_dotenv()

data_service = get_mongo_data_service()

arg_parser = argparse.ArgumentParser(description='Start loading data from local storage to persisted model')
arg_parser.add_argument('-s', dest='start_date', type=str, help='date as ddMMYYYY. Default to last loaded data', required=False)
arg_parser.add_argument('-e', dest='end_date', type=str, help='date as ddMMYYYY. Default to yesterday', required=False)

args = arg_parser.parse_args()

START_DATE = args.start_date or '29032022'
END_DATE = args.end_date or date.strftime(date.today() - timedelta(days=1), settings.DATE_FORMAT)

date_iterator = get_iterator(START_DATE, END_DATE)


DB_URI = os.environ['MODEL_DB_URI']

session = create_session(DB_URI)

race_dao = RaceDao(session)

for date_cursor in date_iterator:

    logging.info(f'Dealing with {get_date_string_from_date(date_cursor)}')
    races = data_service.get_races_by_date(date_cursor)
    with session.begin():
        for race in races:
            saved_race = race_dao.save_race(race)
            logging.info(f'Race {saved_race.name} saved with id {saved_race.id}')
        session.commit()
#
# # races = race_dao.get_race_by_identity(datetime.strptime('29032022', settings.DATE_FORMAT), 1, 6)
# # logging.info(race[0].name)
# # with session.begin():
# for race in races:
#     logging.info(race.name)
#         race_dao.save_race(race)
#         session.commit()`
