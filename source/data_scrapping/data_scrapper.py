from datetime import datetime, date, timedelta
import logging
from source import settings
from pymongo.errors import DuplicateKeyError

from source.date_iterator import get_iterator

ONE_DAY_DURATION = timedelta(days=1)


class DataScrapper():

    def __init__(self, data_service, pmu_api_client):
        self.data_service = data_service
        self.pmu_api_client = pmu_api_client

    def scrap(self, start_date_string=None):
        start_date = self.get_date_as_date(start_date_string) \
            if start_date_string \
            else self.data_service.get_latest_scrapping() + ONE_DAY_DURATION  # + one  because latest scrapping date has been processed

        logging.info("Starting scrapping from date: {}".format(self.get_date_as_string(start_date)))
        date_itr = self.get_until_yesterday_date_iterator(start_date)

        for date_cursor in date_itr:
            date_cursor_string = self.get_date_as_string(date_cursor)
            program_of_the_day = self.pmu_api_client.get_program_of_the_day(date_cursor_string)
            logging.info("Program of {}".format(date_cursor_string))
            try:
                self.data_service.save_program(program_of_the_day, date_cursor_string)
            except DuplicateKeyError:
                logging.warning("Program for {} already exists".format(date_cursor_string))

            for meeting in program_of_the_day["reunions"]:
                meeting_id = meeting["numOfficiel"]
                for race in meeting["courses"]:
                    race_id = race["numOrdre"]
                    logging.info("{} - Meeting {} - Race {} - {}".format(date_cursor_string, meeting_id, race_id,
                                                                         meeting["hippodrome"]["libelleLong"]))

                    participants = self.pmu_api_client.get_participants(date_cursor_string, meeting_id, race_id)
                    try:
                        self.data_service.save_participants(participants, date_cursor_string, meeting_id, race_id)
                    except DuplicateKeyError:
                        logging.warning(
                            "Participants for {}R{}C{} already exists".format(date_cursor_string, meeting_id, race_id))

                    try:
                        participants_detailed_perf = self.pmu_api_client.get_detailed_perf(date_cursor_string, meeting_id,
                                                                                       race_id)
                    except Exception as err:
                        logging.warning(f'Failed to get detailed perf for {date_cursor_string}R{meeting_id}C{race_id}: {err}')

                    try:
                        self.data_service.save_participants_detailed_perf(participants_detailed_perf,
                                                                          date_cursor_string, meeting_id, race_id)
                    except DuplicateKeyError:
                        logging.warning(
                            "Participants details for {}R{}C{} already exists".format(date_cursor_string, meeting_id,
                                                                                      race_id))

        else:
            if date_cursor:
                self.data_service.set_latest_scrapping(date_cursor)

        logging.info('Scrapping finished')

    def get_until_yesterday_date_iterator(self, start_date):
        yesterday = date.today() - ONE_DAY_DURATION
        return get_iterator(start_date, yesterday)

    def get_date_as_date(self, date_string):
        return datetime.strptime(date_string, settings.DATE_FORMAT).date()

    def get_date_as_string(self, date_date):
        return date_date.strftime(settings.DATE_FORMAT)

    def get_date_as_string_from_timestamp(self, time_stamp):
        return self.get_date_as_string(date.fromtimestamp(time_stamp / 1000))
