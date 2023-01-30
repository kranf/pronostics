##
#
#   Generate features and store them as CSV files
#
import csv

from dotenv import load_dotenv
import os

from source.data_service import get_data_service
from source.machine_learning.mapper import to_features, get_feature_list
from source.utils import set_logger

set_logger()

load_dotenv()

DB_URI = os.environ['MODEL_DB_URI']
TRAINING_DATASET_FILE = 'training-dataset.csv'

dataService = get_data_service(DB_URI)

races = dataService.get_all_races()

with open(TRAINING_DATASET_FILE, 'w') as csvfile:
    csvWriter = csv.DictWriter(csvfile, get_feature_list())
    csvWriter.writeheader()
    for race in races:
        feature = to_features(race)
        csvWriter.writerow(feature)
