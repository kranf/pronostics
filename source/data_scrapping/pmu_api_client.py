import requests


class PmuApiClient():
    def __init__(self):
        self.program_url = 'https://online.turfinfo.api.pmu.fr/rest/client/1/programme/{}?meteo=true&specialisation=INTERNET'
        self.participant_url = 'https://online.turfinfo.api.pmu.fr/rest/client/1/programme/{}/R{}/C{}/participants?specialisation=INTERNET'
        self.detailed_perf_url = 'https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{}/R{}/C{}/performances-detaillees/pretty'

    def get_program_of_the_day(self, date):
        """ retrieve the program for the given date.
        Date expected format is ddMMyyyy e.g. 3112020 => 31st december 2020
        """
        url = self.program_url.format(date)
        return requests.get(url).json()["programme"]

    def get_participants(self, date, meeting_id, race_id):
        """ Retreives participants of a race identified by a date (ddMMyyyy),
        a meeting_id and a race_id.
        """
        url = self.participant_url.format(date, meeting_id, race_id)
        return requests.get(url).json()

    def get_detailed_perf(self, date, meeting_id, race_id):
        """ Retreives participants' last performances
        including the drivers and their weight for a race
        identified by a date (ddMMyyyy), meeting_id and a race_id.
        """
        url = self.detailed_perf_url.format(date, meeting_id, race_id)
        return requests.get(url).json()
