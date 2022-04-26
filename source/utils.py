import logging
from datetime import datetime, timedelta, timezone
from source.data_scrapping.data_service import DataService
import os
import pymongo
from dotenv import load_dotenv

def set_logger():
    logging.basicConfig(level=logging.INFO)

def get_date_time_from_timestamp_with_offset(timestamp_in_milliseconds, offset_in_milliseconds):
    tz = timezone(timedelta(seconds=offset_in_milliseconds/1000))
    return datetime.fromtimestamp(timestamp_in_milliseconds/1000, tz)

def get_mongo_data_service():

    mongodb_uri = os.environ['MONGODB_URI']
    db_name = os.environ['DB_NAME']

    client = pymongo.MongoClient(mongodb_uri)
    db = client[db_name]
    return DataService(db)
