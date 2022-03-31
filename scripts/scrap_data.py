import pymongo
import os
import datetime
import pprint
from dotenv import load_dotenv
from source.data_scrapping.data_scrapper import DataScrapper
from source.data_scrapping.pmu_api_client import PmuApiClient

load_dotenv()
pp = pprint.PrettyPrinter()
MONGODB_URI = os.environ['MONGODB_URI']
DB_NAME = os.environ['DB_NAME']

client = pymongo.MongoClient(MONGODB_URI)
db = client[DB_NAME]

pmu_api_client = PmuApiClient()
scrapper = DataScrapper(db, pmu_api_client)
# scrapper.set_latest_scrapping(datetime.date.today().isoformat())
scrapper.scrap("29032022")
