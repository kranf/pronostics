class RaceMapper:
    def __init__(self, race):
        self.race = race

    def to_race_features(self):
        self.validate_race(self.race)
        return {
            'is_diurnal': int(self.race.nature.lower() == 'diurne'),
            'is_nocturnal': int(self.race.nature.lower() == 'nocturne'),
            'is_half_nocturnal': int(self.race.nature.lower() == 'seminocturne'),
            'length_in_meter': self.race.length,
        }

    def to_participants_features(self):
        return [self.to_participant_features(participant) for participant in self.race.participants]

    def to_participant_features(self, participant):
        return {
            f'p{participant.pmu_id}_driver_change': int(participant.driver_change),
            f'p{participant.pmu_id}_lane_id': int(participant.lane_id),
        }

    def validate_race(self):
        assert self.race.nature.lower() in ['diurne', 'nocturne', 'seminocturne']