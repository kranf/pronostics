##
#
#   Generate features and store them as CSV files
#
import logging

from dotenv import load_dotenv
import os

from source.data_service import get_data_service
from source.utils import set_logger
from source.machine_learning.training_dataset_generator import TrainingDatasetGenerator

set_logger()

load_dotenv()

DB_URI = os.environ['MODEL_DB_URI']



dataService = get_data_service(DB_URI)

races = dataService.get_all_races()
generator = TrainingDatasetGenerator()

generator.generate_training_dataset(races)
