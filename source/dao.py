from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from source.model import Base, Horse, Race
from sqlalchemy import select


def create_session(db_uri):
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    return Session(engine)


class HorseDao:
    def __init__(self, session):
        self.session = session

    def save_horse(self, horse):
        self.session.add(horse)

    def get_horse_by_name(self, name):
        statement = select(Horse).where(Horse.name == name)
        horse = self.session.execute(statement)
        return horse


class RaceDao:
    def __init__(self, session):
        self.session = session

    def save_race(self, race):
        return self.session.add(race)

    def get_race_by_identity(self, date, meeting_id, race_id):
        """Identity is aggregation of date, meeting_id and race_id"""
        statement = select(Race).where(Race.start_date > date, Race.meeting_id == meeting_id, Race.race_id == race_id)
        race = self.session.execute(statement).scalars()
        return race
