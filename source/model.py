from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey, UniqueConstraint, Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
            owner=horse_data["proprietaire"] if "proprietaire" in horse_data else None,
            father_name=horse_data["nomPere"] if "nomPere" in horse_data else None,
            mother_name=horse_data["nomMere"] if "nomMere" in horse_data else None,
            trainer=horse_data["entraineur"] if "entraineur" in horse_data else None,
            breeder=horse_data["eleveur"] if "eleveur" in horse_data else None, )


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
    race = relationship("Race", back_populates="participants", lazy="selectin")
    rank = Column(Integer)
    horse_id = Column(Integer, ForeignKey("horse.id"))
    horse = relationship("Horse", lazy="immediate")
    age = Column(Integer)
    driver_name = Column(String, ForeignKey("driver.name"))
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
    prior_horse_distance = Column(Integer)
    speed = Column(Float)
    UniqueConstraint(race_id, horse_id)
 
    def __str__(self):
        return f'{self.horse.name} | pmuId: {self.pmu_id} | Field: {self.race.field} | rank: {self.rank} | lane: {self.lane_id}'
    
    @staticmethod
    def fromJson(participant_data, race_id, horse_id, speed):
        """
        @params: Participant_date as returned participants endpoint
        """
        return Participant(
            race_id=race_id,
            rank=participant_data["ordreArrivee"] if "ordreArrivee" in participant_data else None,
            horse_id=horse_id,
            age=participant_data['age'],
            driver_name=participant_data['driver'] if 'driver' in participant_data else None,
            driver_change=participant_data["driverChange"] if 'driverChange' in participant_data else False,
            pmu_id=participant_data["numPmu"],
            disadvantage_value=participant_data["handicapValeur"] if "handicapValeur" in participant_data else 0,
            disadvantage_weight=participant_data["handicapPoids"] if "handicapPoids" in participant_data else 0,
            disadvantage_length=participant_data[
                "handicapDistance"] if "handicapDistance" in participant_data else 0,
            blinders=participant_data["oeilleres"],
            lane_id=participant_data["placeCorde"] if "placeCorde" in participant_data else -1,
            music=participant_data["musique"],
            pregnent=participant_data["jumentPleine"],
            weighed_duration_km=participant_data[
                "reductionKilometrique"] if "reductionKilometrique" in participant_data else None,
            prior_horse_distance=participant_data["distanceChevalPrecedent"][
                "libelleLong"] if "distanceChevalPrecedent" in participant_data else None,
            speed=speed
        )


class Race(Base):
    __tablename__ = "race"
    id = Column(Integer, primary_key=True)
    meeting_id = Column(String, nullable=False)  # Reunion
    race_id = Column(String, nullable=False)  # Course
    date_string = Column(String)  # date as referred in interfaces
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
    participants = relationship("Participant", back_populates="race", lazy="selectin")
    UniqueConstraint(start_date, race_id, meeting_id)

    def get_pmu_id(self):
        return self.build_pmu_id(self.date_string, self.meeting_id, self.race_id)

    def __str__(self):
        return f'Race {self.get_pmu_id()} | Name {self.name}'
    
    @staticmethod
    def build_pmu_id(date_string, meeting_id, race_id):
        return F'{date_string}R{meeting_id}C{race_id}'

    @staticmethod
    def build_pmu_id_from_race_data(date_string, race_data):
        return Race.build_pmu_id(date_string, race_data['numReunion'], race_data['numOrdre'])

    @staticmethod
    def fromJson(race_data, meeting_data, date_string):
        return Race(
            meeting_id=int(race_data["numReunion"]),
            race_id=int(race_data["numOrdre"]),
            date_string=date_string,
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
            penetrometre_value=race_data["penetrometre"][
                "valeurMesure"] if "penetrometre" in race_data and "valeurMesure" in race_data[
                "penetrometre"] else None,
            racetrack_name=race_data["hippodrome"]["libelleLong"])
