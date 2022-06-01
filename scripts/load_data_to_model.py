import argparse
from datetime import date, timedelta

from dotenv import load_dotenv

from source import settings
from source.dao import RaceDao, create_session, HorseDao
from source.data_scrapping import get_mongo_data_service
from source.date_iterator import get_iterator
from source.model import Race, Participant, Horse, Driver
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
horse_dao = HorseDao(session)

for date_cursor in date_iterator:

    date_string = get_date_string_from_date(date_cursor)
    logging.info(f'Dealing with {date_string}')
    program = data_service.get_program_for_date(date_cursor)

    for meeting in program['reunions']:
        for raw_race in meeting['courses']:
            _race = Race.fromJson(raw_race, meeting, date_string)
            with session.begin():
                race = race_dao.save_race(_race)
                logging.info(f'Race {race.get_pmu_id()}({race.name}) saved with id {race.id}')
                raw_participants = data_service.get_participants_for_race(race)
                for raw_participant in raw_participants:
                    _horse = Horse.fromJson(raw_participant, date_cursor.year - raw_participant['age'])
                    horse = horse_dao.save_horse(_horse)
                    logging.info(f'Horse {horse.name} saved with id {horse.id}')
                    _participant = Participant.fromJson(raw_participant, race.id, horse.id)


                # raw_participants_detailed_perf = data_service.get_participants_detailed_perf_for_race(race)
                # for raw_participants_detailed_perf in raw_participants_detailed_perf:
                #     detailed_perf = filter(lambda participant: participant['nomCheval'] == raw_participant['name'], raw_participants_detailed_perf )
                #     _driver = Driver.fromJson()
                session.commit()
