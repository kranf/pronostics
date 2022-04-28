class DataService:
    def __init__(self, race_dao, horse_dao, driver_dao, participant_dao):
        self.raceDao = race_dao
        self.horseDao = horse_dao
        self.driverDao = driver_dao
        self.participantDao = participant_dao


