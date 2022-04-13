from source.utils import get_date_time_from_timestamp_with_offset

def test_get_date_time_from_timestamp_with_offset():
    timestamp = 1648916820000
    offset = 7200000
    datetime = get_date_time_from_timestamp_with_offset(timestamp, offset)
    assert datetime.hour == 18
    assert datetime.minute == 27
