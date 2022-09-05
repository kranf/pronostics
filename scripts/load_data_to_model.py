import argparse
import logging
import os
from datetime import date, timedelta

from dotenv import load_dotenv

from source import settings
from source.data_scrapping import get_mongo_data_service
from source.data_service import get_data_service
from source.date_iterator import get_iterator
from source.model import Race
from source.utils import set_logger, get_date_string_from_date

set_logger()

load_dotenv()

scrappedDataService = get_mongo_data_service()

arg_parser = argparse.ArgumentParser(description='Start loading data from local storage to persisted model')
arg_parser.add_argument('-s', dest='start_date', type=str, help='date as ddMMYYYY. Default to last loaded data',
                        required=False)
arg_parser.add_argument('-e', dest='end_date', type=str, help='date as ddMMYYYY. Default to yesterday', required=False)

args = arg_parser.parse_args()

START_DATE = args.start_date or '29032022'
END_DATE = args.end_date or date.strftime(date.today() - timedelta(days=1), settings.DATE_FORMAT)

date_iterator = get_iterator(START_DATE, END_DATE)

DB_URI = os.environ['MODEL_DB_URI']

dataService = get_data_service(DB_URI)

for date_cursor in date_iterator:

    date_string = get_date_string_from_date(date_cursor)
    program = scrappedDataService.get_program_for_date(date_cursor)

    for meeting in program['reunions']:
        for raw_race in meeting['courses']:
            pmu_id = Race.build_pmu_id_from_race_data(date_string, raw_race)
            raw_participants = scrappedDataService.get_participants_for_race(pmu_id)
            raw_participants_detailed_perf = scrappedDataService.get_participants_detailed_perf_for_race(pmu_id)
            race = dataService.save_race(raw_race, raw_participants, raw_participants_detailed_perf, meeting, date_cursor)