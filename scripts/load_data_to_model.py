from dotenv import load_dotenv

from source.dao import RaceDao
from source.data_scrapping import get_mongo_data_service
from source.model import Race
from source.utils import set_logger
import logging
import os

set_logger()

load_dotenv()

data_service = get_mongo_data_service()

DB_URI = os.environ['MODEL_DB_URI']
races = data_service.get_races_by_date('29032022')
race_dao = RaceDao(DB_URI)

# for meeting in races['reunions']:
#     for race in meeting['courses']:
#         raceModel = Race.fromJson(race, meeting)
#         race_dao.save_race(raceModel)


for race in races:
    logging.info(race.racetrack_name)