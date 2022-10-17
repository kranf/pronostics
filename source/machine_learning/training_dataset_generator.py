import logging

import pandas as pd
from pandas import concat


class TrainingDatasetGenerator:

    def generate_training_dataset(self, races):
        race_features = []
        for race in races:
            race_features += [self.to_race_feature(race)]
            print(race_features)
        race_data = pd.DataFrame(race_features)
        logging.info(race_data)

    def to_race_feature(self, race):
        self.validate_race(race)
        return {
            'is_diurnal': int(race.nature.lower() == 'diurne'),
            'is_nocturnal': int(race.nature.lower() == 'nocturne'),
            'is_half_nocturnal': int(race.nature.lower() == 'seminocturne')
        }

    def validate_race(self, race):
        assert race.nature in ['diurne', 'nocturne', 'seminocturne']