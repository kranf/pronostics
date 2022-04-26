from dotenv import load_dotenv

from source.dao import RaceDao
from source.model import Race
from source.utils import set_logger, get_mongo_data_service
import logging
import os

set_logger()

load_dotenv()

data_service = get_mongo_data_service()

DB_URI = os.environ['MODEL_DB_URI']
programs = data_service.get_all_programs()
race_dao = RaceDao(DB_URI)

for program in programs:
    for meeting in program['reunions']:
        for race in meeting['courses']:
            raceModel = Race.fromJson(race, meeting)
            race_dao.save_race(raceModel)


races = race_dao.get_race_by_identity('asdf', 2, 3)
for race in races:
    logging.info(race.racetrack_name)