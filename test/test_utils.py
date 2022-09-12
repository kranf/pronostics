from source.data_scrapping.pmu_api_client import PmuApiClient
from source.utils import get_date_time_from_timestamp_with_offset, convert_horse_distance


def test_get_date_time_from_timestamp_with_offset():
    timestamp = 1648916820000
    offset = 7200000
    datetime = get_date_time_from_timestamp_with_offset(timestamp, offset)
    assert datetime.hour == 18
    assert datetime.minute == 27

def test_get_detailed_perf():
    pmu_api_client = PmuApiClient()
    response = pmu_api_client.get_detailed_perf('17022019', 5, 1)
    print(response)

def test_convert_horse_distance():
    distance = '3 L 1/2'
    print(convert_horse_distance(distance))
    return True
