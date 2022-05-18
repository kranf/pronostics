from datetime import datetime

from dotenv import load_dotenv

from source import settings
from source.dao import RaceDao, create_session
from source.data_scrapping import get_mongo_data_service
from source.model import Race
from source.utils import set_logger
import logging
import os

set_logger()

load_dotenv()

data_service = get_mongo_data_service()

DB_URI = os.environ['MODEL_DB_URI']
# races = data_service.get_races_by_date('29032022')

# for meeting in races['reunions']:
#     for race in meeting['courses']:
#         raceModel = Race.fromJson(race, meeting)
#         race_dao.save_race(raceModel)

session = create_session(DB_URI)

race_dao = RaceDao(session)

races = race_dao.get_race_by_identity(datetime.strptime('29032022', settings.DATE_FORMAT), 1, 1)
# logging.info(race[0].name)
# with session.begin():
for race in races:
    logging.info(race.name)
#         race_dao.save_race(race)
#         session.commit()`
