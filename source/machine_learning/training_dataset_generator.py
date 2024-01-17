import logging
from functools import reduce
from operator import add

import pandas as pd
from pandas import concat


class TrainingDatasetGenerator:

    def __init__(self, data_service):
        self.data_service = data_service

    def to_features(self, race):
        feature = self.to_race_features(race)
        for participant in race.participants:
            feature.update(self.to_participant_features(participant))
        return feature

    def to_race_features(self, race):
        self.validate_race(race)
        return {
            'is_diurnal': int(race.nature.lower() == 'diurne'),
            'is_nocturnal': int(race.nature.lower() == 'nocturne'),
            'is_half_nocturnal': int(race.nature.lower() == 'seminocturne'),
            'length_in_meter': race.length,
            'field_is_flat': int(race.field.lower() == 'plat'),
            'field_is_harness': int(race.field.lower() == 'attele'),
            'field_is_hurdle': int(race.field.lower() == 'haie'),
            'field_is_saddle': int(race.field.lower() == 'monte'),
            'field_is_steeplechase': int(race.field.lower() == 'steeplechase'),
            'field_is_cross': int(race.field.lower() == 'cross'),
        }

    def to_participants_features(self, race):
        return [self.to_participant_features(participant) for participant in race.participants]

    def to_participant_features(self, participant):
        return {
            f'p{participant.pmu_id}_driver_change': int(participant.driver_change),
            f'p{participant.pmu_id}_lane_id': int(participant.lane_id),
            f'p{participant.pmu_id}_speed_average': int(self.calculate_average_speed(participant)),
        }

    def validate_race(self, race):
        assert race.nature.lower() in ['diurne', 'nocturne', 'seminocturne']
        assert race.field.lower() in ['plat', 'attele', 'haie', 'monte', 'steeplechase', 'cross']

    def calculate_average_speed(self, participant):
        participations = self.data_service.get_participations_for_horse(participant.horse.name)
        return reduce(add, [p.speed for p in participations])/len(participations)

    # def generate_training_dataset(self, races):
    #     features = []
    #     for race in races:
    #         feature = self.to_race_feature(race)
    #         for participant in race.participants:
    #             feature.update(self.to_participant_feature(participant))
    #         features += [feature]
    #     race_data = pd.DataFrame(features)
    #     logging.info(race_data)