from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from utils import get_date_time_from_timestamp_with_offset

Base = declarative_base()

class Horse(Base):
    __tablename__ = "horse"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    gender = Column(String)
    race = Column(String)
    owner = Column(String)
    father_name = Column(String)
    mother_name = Column(String)
    trainer = Column(String)
    breeder = Column(String)

    @staticmethod
    def fromJson(horseData):
        return Horse(
            name = horseData["nom"],
            gender = horseData["sexe"]
        )


class Driver(Base):
    __tablename__ = "driver"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    weight = Column(Integer)


class Participant(Base):
    __tablename__ = "participant"
    id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey('race.id'))
    rank = Column(Integer)
    horse_id = Column(Integer, ForeignKey("horse.id"))
    horse = relationship("Horse")
    driver_id = Column(Integer, ForeignKey("driver.id"))
    driver = relationship("Driver")
    driver_change = Column(Boolean)
    pmu_id = Column(Integer)
    disadvantage_value = Column(Integer)  # handicapValeur
    disadvantage_weight = Column(Integer)  # handicapPoids
    disadvantage_length = Column(Integer)  # handicapDistance
    blinders = Column(String)
    lane_id = Column(Integer)
    music = Column(String)
    pregnent = Column(Boolean)
    weighed_duration_km = Column(Integer)


class Race(Base):
    __tablename__ = "race"
    id = Column(Integer, primary_key=True)
    meeting_id = Column(String, nullable=False) # Reunion
    race_id = Column(String, nullable=False)    # Course
    start_date = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)   # Libelle
    length = Column(Integer)
    length_unit = Column(String)
    turn = Column(String)   # Corde
    nature = Column(String) # e.g. DIURNE
    field = Column(String)  # Discipline
    specialty = Column(String)   # specialite
    specialty_category = Column(String)   # categorieParticularite
    gender_condition = Column(String)
    age_condition = Column(String)
    conditions = Column(String)
    duration = Column(Integer)
    number_of_participants = Column(Integer)
    penetrometre_value = Column(Integer)
    racetrack_name = Column(String)
    racetrack_type = Column(String)
    participants = relationship("Participant")

    @staticmethod
    def fromJson(race_data, meeting_data):
        return Race(
            meeting_id = race_data["numReunion"],
            race_id = race_data["numOrdre"]
            start_date = get_date_time_from_timestamp_with_offset(race_data["heureDepart"], race_data["timezoneOffset"])
            name = race_data["libelle"]
            length = race_data["distance"]
            length_unit = race_data["distanceUnit"]
            turn = race_data["corde"]
            nature = meeting_data["nature"]
            field = race_data["discipline"]
            specialty = race_data["specialite"]
            specialty_category = race_data["categorieParticularite"]
            gender_condition = race_data["conditionSexe"]
            age_condition = race_data["conditionAge"]
            conditions = race_data["conditions"]
            duration = race_data["dureeCourse"]
            number_of_participants = race_data["nombreDeclaresPartants"]
            penetrometre_value = race_data["penetrometre"]["valeurMesure"]
            racetrack_name = race_data["hippodrome"]["libelleLong"]
        )
