##
#
#   Generate features and store them as CSV files
#
import csv

from dotenv import load_dotenv
import os
import pandas as pd

from source.data_service import get_data_service
from source.machine_learning.mapper import to_features, get_feature_list
from source.machine_learning.training_dataset_generator import TrainingDatasetGenerator
from source.utils import set_logger

set_logger()

load_dotenv()

DB_URI = os.environ['MODEL_DB_URI']
TRAINING_DATASET_FILE = 'training-dataset.csv'

dataService = get_data_service(DB_URI)
generator = TrainingDatasetGenerator(dataService)

races = dataService.get_all_races()

race_series = pd.Series()
for race in races:
    features = pd.Series(generator.to_features(race))
    race_series = pd.concat([race_series, features])
    print(features)