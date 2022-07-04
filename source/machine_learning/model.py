from source.model import Race


class Season:
    WINTER = 0
    SPRING = 1
    SUMMER = 2
    AUTUMN = 3

def to_features(race, participant):
    race_details = {
        'turn_left': True if race.turn == 'CORDE_GAUCHE' else False,
        'turn_right': True if race.turn == 'CORDE_DROITE' else False,
        'daytime': True if race.nature == 'DIURNE' else False,
        'evening_time': True if race.nature == 'SEMINOCTURNE' else False,
        'night_time': True if race.nature == 'NOCTURNE' else False,
    }
    participant_details = {
        'is_male': True if participant.horse.gender == 'MALES' else False,
        'is_female': True if participant.horse.gender == 'FEMELLES' else False,
        'driver_change': participant.driver_change,
        'disadvantage_value': participant.disadvantage_value,
        'disadvantage_length': participant.disadvantage_length,
        'disadvantage_weight': participant.disadvantage_weight,
        'disadvantage_value_mean': participant.disadvantage_value,
        'disadvantage_length_mean': participant.disadvantage_length,
        'disadvantage_weight_mean': participant.disadvantage_weight,

    }