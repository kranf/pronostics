import logging

from sqlalchemy.orm import sessionmaker

from source import RaceDao
from source.dao import ParticipantDao, DriverDao, HorseDao, SessionProxy, get_engine
from source.model import Race, Horse, Participant, Driver
from source.utils import get_date_string_from_date


def get_data_service(db_uri):
    engine = get_engine(db_uri)
    sessionProxy = SessionProxy()
    raceDao = RaceDao(sessionProxy)
    horseDao = HorseDao(sessionProxy)
    driverDao = DriverDao(sessionProxy)
    participantDao = ParticipantDao(sessionProxy)
    return DataService(engine, sessionProxy, raceDao, horseDao, driverDao, participantDao)


class DataService:
    def __init__(self, engine, session_proxy, race_dao, horse_dao, driver_dao, participant_dao):
        self.sessionMaker = sessionmaker(engine, expire_on_commit=False)
        self.sessionProxy = session_proxy
        self.raceDao = race_dao
        self.horseDao = horse_dao
        self.driverDao = driver_dao
        self.participantDao = participant_dao

    def get_race(self, date_string, meeting_id, race_id):
        with self.sessionMaker.begin() as session:
            self.sessionProxy.set_new_session(session)
            return self.raceDao.get_race_by_pmu_id(date_string, meeting_id, race_id)

    def save_race(self, raw_race, raw_participants, raw_participants_detailed_perf, meeting_data, program_date):

        date_string = get_date_string_from_date(program_date)

        with self.sessionMaker.begin() as session:
            self.sessionProxy.set_new_session(session)
            race = Race.fromJson(raw_race, meeting_data, date_string)
            logging.info(f'Dealing with {race.get_pmu_id()}')

            saved_race = self.raceDao.save_race(race)

            # length seems to be in meters
            if saved_race.length_unit != 'METRE':
                raise RuntimeError(f'Unsupported race length unit: {saved_race.length_unit}')

            raw_participants.sort(key=lambda element: element.rank)
            distance_at_arrival = saved_race.length
            for raw_participant in raw_participants:
                _horse = Horse.fromJson(raw_participant, program_date.year - raw_participant['age'])
                horse = self.horseDao.save_horse(_horse)
                logging.info(f'Horse {horse.name} saved with id {horse.id}')
                distance_at_arrival = distance_at_arrival - convert_horse_distance(raw_participant['distanceChevalPrecedent'])
                speed = distance_at_arrival / saved_race.duration
                _participant = Participant.fromJson(raw_participant, race.id, horse.id, speed)
                participant = self.participantDao.save_participant(_participant)
                logging.info(f'Saving {participant.horse.name} for race {race.get_pmu_id()}')

            ordered_participants = sorted(saved_race.participants, key=lambda element: element.rank)
            logging.debug(f'================== ordered participant =================')
            logging.debug(saved_race.participants)
            for participant in ordered_participants:
                print(participant.rank, participant.prior_horse_distance)

            if len(raw_participants_detailed_perf) > 0:
                for raw_participant_detailed_perf in raw_participants_detailed_perf:
                    for participant_race in raw_participant_detailed_perf['coursesCourues']:
                        for driver_details in participant_race['participants']:
                            if 'poidsJockey' in driver_details:
                                _driver = Driver.fromJson(driver_details['nomJockey'],
                                                          driver_details['poidsJockey'])
                                driver = self.driverDao.save_driver(_driver)
                                logging.info(f'Driver {driver.name} saved with id {driver.id}')

            session.commit()
            return saved_race
