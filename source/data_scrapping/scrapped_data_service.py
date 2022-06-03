from datetime import datetime
from source import settings
import pymongo
from source.model import Race
from source.utils import get_date_string_from_date

RACE_PMU_ID = 'race_pmu_id'


class ScrappedDataService:

    def __init__(self, mongo_db):
        self.mongo_db = mongo_db
        self._create_indexes()

    def _create_indexes(self):
        self.mongo_db.programs.create_index([("date_string", pymongo.ASCENDING)], unique=True)
        self.mongo_db.participants.create_index([(RACE_PMU_ID, pymongo.ASCENDING)], unique=True)
        self.mongo_db.participants_detailed_perf.create_index([(RACE_PMU_ID, pymongo.ASCENDING)], unique=True)

    def get_latest_scrapping(self):
        date_latest = self.mongo_db.latest_scrapping.find_one()["latest"]
        return datetime.strptime(date_latest, settings.DATE_FORMAT).date()

    def set_latest_scrapping(self, _date):
        current_latest = self.get_latest_scrapping()
        if not _date > current_latest:
            return

        self.mongo_db.latest_scrapping.delete_many({})
        return self.mongo_db.latest_scrapping.insert_one({"latest": _date.strftime(settings.DATE_FORMAT)})

    def save_program(self, program, date_string):
        """ :param: date_string ddMMYYYY date of the program
            :param: program: array of reunions e.g.
            "reunions": [
      {
        "cached": false,
        "timezoneOffset": 3600000,
        "dateReunion": 1647817200000,
        "numOfficiel": 1,
        "numOfficielReunionPrecedente": null,
        "numOfficielReunionSuivante": 2,
        "numExterne": 1,
        "nature": "DIURNE",
        "hippodrome": {
          "code": "COM",
          "libelleCourt": "COMPIEGNE",
          "libelleLong": "HIPPODROME DE COMPIEGNE"
        },
        "pays": {
          "code": "FRA",
          "libelle": "FRANCE"
        },
        "courses": [
          {
            "cached": false,
            "departImminent": false,
            "arriveeDefinitive": true,
            "timezoneOffset": 3600000,
            "numReunion": 1,
            "numExterneReunion": 1,
            "numOrdre": 1,
            "numExterne": 1,
            "heureDepart": 1647867000000,
            "libelle": "PRIX DE LA PLAINE DU PUTOIS",
            "libelleCourt": "PLAINE PUTOIS",
            "montantPrix": 50000,
            "parcours": "1800 M.",
            "distance": 1800,
            "distanceUnit": "METRE",
            "corde": "CORDE_GAUCHE",
            "discipline": "PLAT",
            "specialite": "PLAT",
            "categorieParticularite": "HANDICAP_DIVISE",
            "conditionAge": "QUATRE_ANS_ET_PLUS",
            "conditionSexe": "TOUS_CHEVAUX",
            "nombreDeclaresPartants": 15,
            "grandPrixNationalTrot": false,
            "numSocieteMere": 4382,
            "pariMultiCourses": false,
            "pariSpecial": false,
            "montantTotalOffert": 50000,
            "montantOffert1er": 25000,
            "montantOffert2eme": 9500,
            "montantOffert3eme": 7000,
            "montantOffert4eme": 4000,
            "montantOffert5eme": 2000,
            "conditions": "Pour chevaux entiers, hongres et jume nts de 4 ans et au-dessus, ayant cour u depuis le 21 septembre 2021 inclus.",
            "numCourseDedoublee": 1,
            "paris": [
              {
                "combine": false,
                "spotAutorise": false,
                "ordre": false,
                "complement": false,
                "codePari": "E_SIMPLE_GAGNANT",
                "nbChevauxReglementaire": 1,
                "typePari": "E_SIMPLE_GAGNANT",
                "miseBase": 100,
                "enVente": false,
                "audience": "NATIONAL",
                "reportable": true,
                "infosJackpot": {
                  "miseBase": 150,
                  "tauxContribution": {
                    "numerateur": 1,
                    "denominateur": 3
                  }
                }
              },
              {
                "combine": false,
                "spotAutorise": false,
                "ordre": false,
                "complement": false,
                "codePari": "E_SIMPLE_PLACE",
                "nbChevauxReglementaire": 1,
                "typePari": "E_SIMPLE_PLACE",
                "miseBase": 100,
                "enVente": false,
                "audience": "NATIONAL",
                "reportable": true,
                "infosJackpot": {
                  "miseBase": 150,
                  "tauxContribution": {
                    "numerateur": 1,
                    "denominateur": 3
                  }
                }
              },
              {
                "combine": false,
                "spotAutorise": false,
                "ordre": false,
                "complement": false,
                "codePari": "E_REPORT_PLUS",
                "nbChevauxReglementaire": 1,
                "typePari": "E_REPORT_PLUS",
                "enVente": false,
                "reportable": false
              },
              {
                "combine": true,
                "spotAutorise": true,
                "ordre": false,
                "complement": true,
                "codePari": "E_COUPLE_GAGNANT",
                "nbChevauxReglementaire": 2,
                "typePari": "E_COUPLE_GAGNANT",
                "miseBase": 100,
                "enVente": false,
                "audience": "NATIONAL",
                "reportable": true
              },
              {
                "combine": true,
                "spotAutorise": true,
                "ordre": false,
                "complement": true,
                "codePari": "E_COUPLE_PLACE",
                "nbChevauxReglementaire": 2,
                "typePari": "E_COUPLE_PLACE",
                "miseBase": 100,
                "enVente": false,
                "audience": "NATIONAL",
                "reportable": true
              },
              {
                "combine": true,
                "spotAutorise": true,
                "valeursFlexiAutorisees": [
                  50
                ],
                "ordre": false,
                "complement": true,
                "codePari": "E_DEUX_SUR_QUATRE",
                "nbChevauxReglementaire": 2,
                "typePari": "E_DEUX_SUR_QUATRE",
                "miseBase": 300,
                "enVente": false,
                "audience": "NATIONAL",
                "reportable": true,
                "infosJackpot": {
                  "miseBase": 400,
                  "tauxContribution": {
                    "numerateur": 1,
                    "denominateur": 4
                  }
                }
              },
              {
                "combine": true,
                "spotAutorise": true,
                "valeursFlexiAutorisees": [
                  50
                ],
                "ordre": false,
                "complement": false,
                "codePari": "E_MULTI",
                "nbChevauxReglementaire": 4,
                "valeursRisqueAutorisees": [
                  4,
                  5,
                  6,
                  7
                ],
                "typePari": "E_MULTI",
                "miseBase": 300,
                "enVente": false,
                "audience": "NATIONAL",
                "reportable": false
              },
              {
                "combine": true,
                "spotAutorise": true,
                "valeursFlexiAutorisees": [
                  50
                ],
                "ordre": true,
                "complement": true,
                "codePari": "E_TIERCE",
                "nbChevauxReglementaire": 3,
                "typePari": "E_TIERCE",
                "miseBase": 100,
                "enVente": false,
                "audience": "NATIONAL",
                "reportable": false
              },
              {
                "combine": true,
                "spotAutorise": true,
                "valeursFlexiAutorisees": [
                  50
                ],
                "ordre": true,
                "complement": true,
                "codePari": "E_QUARTE_PLUS",
                "nbChevauxReglementaire": 4,
                "typePari": "E_QUARTE_PLUS",
                "miseBase": 150,
                "enVente": false,
                "audience": "NATIONAL",
                "reportable": false
              },
              {
                "combine": true,
                "spotAutorise": true,
                "valeursFlexiAutorisees": [
                  25,
                  50
                ],
                "ordre": true,
                "complement": true,
                "codePari": "E_QUINTE_PLUS",
                "nbChevauxReglementaire": 5,
                "typePari": "E_QUINTE_PLUS",
                "miseBase": 200,
                "enVente": false,
                "audience": "NATIONAL",
                "reportable": false,
                "nouveauQuinte": true
              },
              {
                "combine": false,
                "spotAutorise": false,
                "ordre": true,
                "complement": false,
                "codePari": "E_TIC_TROIS",
                "nbChevauxReglementaire": 5,
                "typePari": "E_TIC_TROIS",
                "miseBase": 450,
                "enVente": false,
                "audience": "NATIONAL",
                "reportable": false
              }
            ],
            "statut": "FIN_COURSE",
            "categorieStatut": "ARRIVEE",
            "dureeCourse": 110000,
            "participants": [],
            "ecuries": [],
            "penetrometre": {
              "valeurMesure": "3,7",
              "heureMesure": "2022-03-21T10:30",
              "intitule": "Souple",
              "commentaire": ""
            },
            "rapportsDefinitifsDisponibles": true,
            "isArriveeDefinitive": true,
            "isDepartImminent": false,
            "isDepartAJPlusUn": false,
            "cagnottes": [],
            "pronosticsExpires": true,
            "replayDisponible": true,
            "hippodrome": {
              "codeHippodrome": "COM",
              "libelleCourt": "COMPIEGNE",
              "libelleLong": "HIPPODROME DE COMPIEGNE"
            },
            "epcPourTousParis": true,
            "numQuestion": [
              1
            ],
            "courseTrackee": false,
            "courseExclusiveInternet": false,
            "formuleChampLibreIndisponible": false,
            "hasEParis": true,
            "ordreArrivee": [
              [
                1
              ],
              [
                2
              ],
              [
                3
              ],
              [
                11
              ],
              [
                6
              ],
              [
                8
              ],
              [
                9
              ],
              [
                12
              ],
              [
                13
              ],
              [
                7
              ],
              [
                10
              ],
              [
                5
              ],
              [
                14
              ],
              [
                15
              ],
              [
                4
              ]
            ]
          }]]
        """
        program["date_string"] = date_string
        return self.mongo_db.programs.insert_one(program)

    def save_participants(self, participants, date, meeting_id, race_id):
        """:param participants
            e.g. 
            [{
              "nom": "MRS. SUE BG",
              "numPmu": 1,
              "age": 6,
              "sexe": "FEMELLES",
              "race": "TROTTEUR ETRANGER",
              "statut": "PARTANT",
              "placeCorde": 1,
              "oeilleres": "SANS_OEILLERES",
              "proprietaire": "PETER RISS",
              "entraineur": "P. RISS",
              "driver": "OPPOLI RALF",
              "driverChange": false,
              "indicateurInedit": false,
              "musique": "3a4a2a8a9a5a4a5a4a5a",
              "nombreCourses": 0,
              "nombreVictoires": 0,
              "nombrePlaces": 0,
              "nombrePlacesSecond": 0,
              "nombrePlacesTroisieme": 0,
              "gainsParticipant": {
                "gainsCarriere": 330000,
                "gainsVictoires": 0,
                "gainsPlace": 0,
                "gainsAnneeEnCours": 0,
                "gainsAnneePrecedente": 0
              },
              "nomPere": "CANTAB HALL DE",
              "nomMere": "COUNTRY KAY SUE",
              "ordreArrivee": 7,
              "jumentPleine": false,
              "engagement": false,
              "supplement": 0,
              "handicapDistance": 2100,
              "poidsConditionMonteChange": false,
              "tempsObtenu": 165530,
              "reductionKilometrique": 78800,
              "dernierRapportDirect": {
                "typePari": "E_SIMPLE_GAGNANT",
                "rapport": 56,
                "typeRapport": "DIRECT",
                "indicateurTendance": " ",
                "nombreIndicateurTendance": 0,
                "dateRapport": 1647858987000,
                "permutation": 1,
                "favoris": false,
                "numPmu1": 1,
                "grossePrise": false
              },
              "dernierRapportReference": {
                "typePari": "E_SIMPLE_GAGNANT",
                "rapport": 33,
                "typeRapport": "REFERENCE",
                "indicateurTendance": "+",
                "nombreIndicateurTendance": 4.36,
                "dateRapport": 1647858605000,
                "permutation": 1,
                "favoris": false,
                "numPmu1": 1,
                "grossePrise": false
              },
              "urlCasaque": "https://www.pmu.fr/back-assets/hippique/casaques/21032022/R2/C1/P1.png",
              "allure": "TROT"
            }]
        """
        participants[RACE_PMU_ID] = Race.build_pmu_id(date, meeting_id, race_id)
        return self.mongo_db.participants.insert_one(participants)

    def save_participants_detailed_perf(self, participants_detailed_perf, date, meeting_id, race_id):
        participants_detailed_perf[RACE_PMU_ID] = Race.build_pmu_id(date, meeting_id, race_id)
        return self.mongo_db.participants_detailed_perf.insert_one(participants_detailed_perf)

    def get_all_programs(self):
        return self.mongo_db.programs.find()

    def get_program_for_date(self, date_of_the_races):
        """ :param date_of_the_races of the program as string ddMMYYYY or date"""

        _date = date_of_the_races if isinstance(date_of_the_races, str) else get_date_string_from_date(
            date_of_the_races)
        return self.mongo_db.programs.find_one({"date_string": _date})

    def get_participants_for_race(self, race):
        """ :param race """

        return self.mongo_db.participants.find_one({RACE_PMU_ID: race.get_pmu_id()})['participants']

    def get_participants_detailed_perf_for_race(self, race):
        """ :param race """

        result = self.mongo_db.participants_detailed_perf.find_one({"pmu_id": race.get_pmu_id()})
        return result['participants'] if result and 'participants' in result else []
