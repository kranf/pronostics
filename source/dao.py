from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from source.model import Base, Horse, Race, Driver, Participant
from sqlalchemy import select


def create_session(db_uri):
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    return Session(engine)


class DriverDao:
    def __init__(self, session):
        self.session = session

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
    def __init__(self, session):
        self.session = session

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
    def __init__(self, session):
        self.session = session

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


class RaceDao:
    def __init__(self, session):
        self.session = session

    def save_race(self, race):
        if not self.get_race_by_pmu_id(race.date_string, race.meeting_id, race.race_id):
            self.session.add(race)

        return self.get_race_by_pmu_id(race.date_string, race.meeting_id, race.race_id)

    def get_race_by_pmu_id(self, date, meeting_id, race_id):
        """pmu id is aggregation of date, meeting_id and race_id"""
        statement = select(Race).where(Race.date_string == date, Race.meeting_id == meeting_id, Race.race_id == race_id)
        result = self.session.execute(statement).scalars().all()
        if len(result) == 0:
            return None

        if len(result) > 1:
            raise RuntimeError()

        return result[0]
