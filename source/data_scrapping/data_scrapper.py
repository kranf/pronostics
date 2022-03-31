from datetime import datetime, date, timedelta
import pprint

DATE_FORMAT = "%d%m%Y"
ONE_DAY_DURATION = timedelta(days=1)

class DataScrapper():

    def __init__(self, mongo_db, pmu_api_client):
        self.mongo_db = mongo_db
        self.pmu_api_client = pmu_api_client

    def scrap(self, start_date_string=None):
        start_date = self.get_date_as_date(start_date_string) \
                        if start_date_string \
                        else self.get_latest_scrapping() + ONE_DAY_DURATION # + one  because latest scrapping date has been processed

        date_itr = self.get_until_yesterday_date_iterator(start_date)

        for date_cursor in date_itr:
            date_cursor_string = self.get_date_as_string(date_cursor)
            program = self.pmu_api_client.get_program_of_the_day(date_cursor_string)
            self.save_program(program)
            saved_programs = self.get_programs()

            for saved_program in saved_programs:

                pprint.pprint("Date: {}".format(self.get_date_as_string_from_timestamp(saved_program["date"])))
                for meeting in saved_program["reunions"]:
                    pprint.pprint("Meeting id: {} \t- date: {}".format(meeting["numOfficiel"], self.get_date_as_string_from_timestamp(meeting["dateReunion"])))
        else:
            if date_cursor:
                self.set_latest_scrapping(date_cursor)

    def save_program(self, program_json):
        return self.mongo_db.programs.insert_one(program_json)

    def get_programs(self):
        return self.mongo_db.programs.find()

    def get_latest_scrapping(self):
        date_latest = self.mongo_db.latest_scrapping.find_one()["latest"]
        return datetime.strptime(date_latest, DATE_FORMAT).date()

    def set_latest_scrapping(self, _date):
        self.mongo_db.latest_scrapping.delete_many({})
        return self.mongo_db.latest_scrapping.insert_one({"latest": self.get_date_as_string(_date)})

    def get_until_yesterday_date_iterator(self, start_date):
        yesterday = date.today() - ONE_DAY_DURATION
        return DateIterable(start_date, yesterday)

    def get_date_as_date(self, date_string):
        return datetime.strptime(date_string, DATE_FORMAT).date()

    def get_date_as_string(self, date_date):
        return date_date.strftime(DATE_FORMAT)

    def get_date_as_string_from_timestamp(self, time_stamp):
        return self.get_date_as_string(date.fromtimestamp(time_stamp/1000))

class DateIterable:

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        return self

    def __next__(self):
        if self._present_day >= self.end_date:
            raise StopIteration
        today = self._present_day
        self._present_day += timedelta(days=1)
        return today
