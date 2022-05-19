from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .utils import get_date_time_from_timestamp_with_offset

Base = declarative_base()


class Horse(Base):
    __tablename__ = "horse"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True, unique=True)
    birth_year = Column(Integer)
    gender = Column(String)
    race = Column(String)
    owner = Column(String)
    father_name = Column(String)
    mother_name = Column(String)
    trainer = Column(String)
    breeder = Column(String)

    @staticmethod
    def fromJson(horse_data, birth_year):
        return Horse(
            name=horse_data["nom"],
            birth_year=birth_year,
            gender=horse_data["sexe"],
            race=horse_data["race"],
            owner=horse_data["proprietaire"],
            father_name=horse_data["nomPere"],
            mother_name=horse_data["nomMere"],
            trainer=horse_data["entraineur"],
            breeder=horse_data["eleveur"])


class Driver(Base):
    __tablename__ = "driver"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    weight = Column(Integer)

    @staticmethod
    def fromJson(name, weight):
        return Driver(
            name=name,
            weight=weight)


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

    @staticmethod
    def fromJson(participant_data, race_id, horse_id, driver_id):
        """
        @params: Participant_date as returned participants endpoint
        """
        return Participant(
            race_id=race_id, rank=participant_data["ordreArrivee"], horse_id=horse_id, driver_id=driver_id,
            driver_change=participant_data["driverChange"], pmu_id=participant_data["numPmu"],
            disadvantage_value=participant_data["handicapValeur"], disadvantage_weight=participant_data["handicapPoids"],
            disadvantage_length=participant_data["handicapDistance"], blinders=participant_data["oeilleres"],
            lane_id=participant_data["placeCorde"], music=participant_data["musique"],
            pregnent=participant_data["jumentPleine"], weighed_duration_km=participant_data["reductionKilometrique"])


class Race(Base):
    __tablename__ = "race"
    id = Column(Integer, primary_key=True)
    meeting_id = Column(String, nullable=False)  # Reunion
    race_id = Column(String, nullable=False)  # Course
    start_date = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)  # Libelle
    length = Column(Integer)
    length_unit = Column(String)
    turn = Column(String)  # Corde
    nature = Column(String)  # e.g. DIURNE
    field = Column(String)  # Discipline
    specialty = Column(String)  # specialite
    specialty_category = Column(String)  # categorieParticularite
    gender_condition = Column(String)
    age_condition = Column(String)
    conditions = Column(String)
    duration = Column(Integer)
    number_of_participants = Column(Integer)
    penetrometre_value = Column(Integer)
    racetrack_name = Column(String)
    racetrack_type = Column(String)
    participants = relationship("Participant")
    UniqueConstraint(start_date, race_id, meeting_id)

    @staticmethod
    def fromJson(race_data, meeting_data):
        return Race(
            meeting_id=int(race_data["numReunion"]),
            race_id=int(race_data["numOrdre"]),
            start_date=get_date_time_from_timestamp_with_offset(race_data["heureDepart"], race_data["timezoneOffset"]),
            name=race_data["libelle"],
            length=race_data["distance"],
            length_unit=race_data["distanceUnit"],
            turn=race_data["corde"] if "corde" in race_data else None,
            nature=meeting_data["nature"],
            field=race_data["discipline"],
            specialty=race_data["specialite"],
            specialty_category=race_data["categorieParticularite"],
            gender_condition=race_data["conditionSexe"],
            age_condition=race_data["conditionAge"] if "conditionAge" in race_data else None,
            conditions=race_data["conditions"],
            duration=race_data["dureeCourse"] if "dureeCourse" in race_data else None,
            number_of_participants=race_data["nombreDeclaresPartants"],
            penetrometre_value=race_data["penetrometre"]["valeurMesure"] if "penetrometre" in race_data and "valeurMesure" in race_data["penetrometre"] else None,
            racetrack_name=race_data["hippodrome"]["libelleLong"])
