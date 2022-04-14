from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from source.model import Base, Horse
from sqlalchemy import select


class HorseDao():
    __init__(self, db_uri):
        engine = create_engine(DB_URI)
        Base.metadata.create_all(engine) # here we create all tables
        Session = sessionmaker(bind=engine)
        self.session = Session()

    save_horse(self, horse):
        self.session.add(horse)

    get_horse_by_name(name):
        statement = select(Horse).where(Horse.name == name)
        horse = self.session.execute(statement).
        return horse
