from source.model import Base, Horse, Race, Driver, Participant
from sqlalchemy import select, create_engine


def get_engine(db_uri):
    engine = create_engine(db_uri, future=True, )
    Base.metadata.create_all(engine)
    return engine


class SessionProxy:
    '''Session proxy should implement ORM session interface as used by DAO
    The proxy is shared accross DAOs
    The real session is handled at higher layer.
    The transaction life cycle begin/commit/rollback/close can be shared across several domain DAOs.
    '''
    def __init__(self):
        self.session = None

    def set_new_session(self, session):
        self.session = session

    def add(self, domainObject):
        return self.session.add(domainObject)

    def execute(self, statement):
        return self.session.execute(statement)


class DriverDao:
    def __init__(self, session_proxy):
        self.session = session_proxy

    def save_driver(self, driver):
        if not self.get_driver_by_name(driver.name):
            self.session.add(driver)
        return self.get_driver_by_name(driver)

    def get_driver_by_name(self, name):
        statement = select(Driver).where(Driver.name == name)
        result = self.session.execute(statement).scalars().all()
        if len(result) == 0:
            return None

        if len(result) > 1:
            raise RuntimeError()

        return result[0]


class HorseDao:
    def __init__(self, session_proxy):
        self.session = session_proxy

    def save_horse(self, horse):
        if not self.get_horse_by_name(horse.name):
            self.session.add(horse)
        return self.get_horse_by_name(horse.name)

    def get_horse_by_name(self, name):
        statement = select(Horse).where(Horse.name == name)
        result = self.session.execute(statement).scalars().all()
        if len(result) == 0:
            return None

        if len(result) > 1:
            raise RuntimeError()

        return result[0]


class ParticipantDao:
    def __init__(self, session_proxy):
        self.session = session_proxy

    def save_participant(self, participant):
        if not self.get_participant_by_race(participant.race_id, participant.horse_id):
            self.session.add(participant)
        return self.get_participant_by_race(participant.race_id, participant.horse_id)

    def get_participant_by_race(self, race_id, horse_id):
        statement = select(Participant).where(Participant.race_id == race_id, Participant.horse_id == horse_id)
        result = self.session.execute(statement).scalars().all()
        if len(result) == 0:
            return None

        if len(result) > 1:
            raise RuntimeError()

        return result[0]

    def get_participations_for_horse(self, horse_id):
        statement = select(Participant).where(Participant.horse_id == horse_id)
        result = self.session.execute(statement).scalars().unique().all()

        return result

class RaceDao:
    def __init__(self, session_proxy):
        self.session = session_proxy

    def save_race(self, race):
        if not self.get_race_by_pmu_id(race.date_string, race.meeting_id, race.race_id):
            self.session.add(race)

        return self.get_race_by_pmu_id(race.date_string, race.meeting_id, race.race_id)

    def get_race_by_pmu_id(self, date, meeting_id, race_id):
        """pmu id is aggregation of date, meeting_id and race_id"""
        statement = select(Race).where(Race.date_string == date, Race.meeting_id == meeting_id, Race.race_id == race_id)
        return self.session.execute(statement).scalars().one()

    def get_all(self):
        statement = select(Race).execution_options(yield_per=10)
        result = self.session.execute(statement).scalars()
        return result