RACE_FEATURE_LIST = [
    'is_diurnal',
    'is_nocturnal',
    'is_half_nocturnal',
    'length_in_meter',
]


PARTICIPANT_FEATURE_LIST = [
    'p{pmu_id}_driver_change',
    'p{pmu_id}_lane_id',
]


def get_feature_list(max_number_of_participant=22):
    return [feature_name.format(pmu_id=pmu_id)
                for feature_name in PARTICIPANT_FEATURE_LIST
                for pmu_id in range(1, max_number_of_participant) ] + RACE_FEATURE_LIST


def to_features(race):
    feature = to_race_features(race)
    for participant in race.participants:
        feature.update(to_participant_features(participant))
    return feature

def to_race_features(race):
    validate_race(race)
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


def to_participants_features(race):
    return [to_participant_features(participant) for participant in race.participants]


def to_participant_features(participant):
    return {
        f'p{participant.pmu_id}_driver_change': int(participant.driver_change),
        f'p{participant.pmu_id}_lane_id': int(participant.lane_id),
    }


def validate_race(race):
    assert race.nature.lower() in ['diurne', 'nocturne', 'seminocturne']
    assert race.field.lower() in ['plat', 'attele', 'haie', 'monte', 'steeplechase', 'cross']