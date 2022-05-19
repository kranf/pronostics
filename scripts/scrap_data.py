from dotenv import load_dotenv

from source.data_scrapping import get_mongo_data_service
from source.data_scrapping.data_scrapper import DataScrapper
from source.data_scrapping.pmu_api_client import PmuApiClient
from source.utils import set_logger

set_logger()

load_dotenv()

data_service = get_mongo_data_service()
pmu_api_client = PmuApiClient()
scrapper = DataScrapper(data_service, pmu_api_client)
scrapper.scrap("22032022")
