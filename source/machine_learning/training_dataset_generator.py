import logging

import pandas as pd
from pandas import concat


class TrainingDatasetGenerator:

    def generate_training_dataset(self, races):
        features = []
        for race in races:
            feature = self.to_race_feature(race)
            for participant in race.participants:
                feature.update(self.to_participant_feature(participant))
            features += [feature]
        race_data = pd.DataFrame(features)
        logging.info(race_data)

    def to_race_feature(self, race):
        self.validate_race(race)
        return {
            'is_diurnal': int(race.nature.lower() == 'diurne'),
            'is_nocturnal': int(race.nature.lower() == 'nocturne'),
            'is_half_nocturnal': int(race.nature.lower() == 'seminocturne'),
            'length_in_meter': race.length,
        }

    def to_participant_feature(self, participant):
        return {
            f'p{participant.pmu_id}_driver_change': int(participant.driver_change),
            f'p{participant.pmu_id}_lane_id': int(participant.lane_id),
        }
    def validate_race(self, race):
        assert race.nature.lower() in ['diurne', 'nocturne', 'seminocturne']