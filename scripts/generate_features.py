##
#
#   Generate features and store them as CSV files
#
import logging

from dotenv import load_dotenv
import os

from sqlalchemy.future import create_engine, select
from sqlalchemy.orm import Session
from source.data_service import get_data_service
from source.model import Race
from source.utils import set_logger

set_logger()

load_dotenv()

DB_URI = os.environ['MODEL_DB_URI']



dataService = get_data_service(DB_URI)

race = dataService.get_race('29032022', 1, 3);

logging.info(race.get_pmu_id())
logging.info([(participant.horse.name, participant.driver_name) for participant in race.participants])
