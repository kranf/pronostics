from source.data_scrapping.scrapped_data_service import ScrappedDataService
import os
import pymongo


def get_mongo_data_service():
    mongodb_uri = os.environ['MONGODB_URI']
    db_name = os.environ['DB_NAME']

    client = pymongo.MongoClient(mongodb_uri)
    db = client[db_name]
    return ScrappedDataService(db)
