import datetime

from ravenpackapi.utils.date_formats import as_datetime, as_datetime_str


def test_date_inputs():
    expected_date = datetime.datetime(2018, 1, 1)
    assert as_datetime('2018-01-01') == expected_date
    expected_datetime = datetime.datetime(2018, 1, 1, 10, 10)
    assert as_datetime('2018-01-01 10:10') == expected_datetime
    assert as_datetime('2018-01-01 10:10:00') == expected_datetime
    assert as_datetime(expected_datetime) == expected_datetime


def test_ignore_trimmed_spaces():
    expected_datetime = datetime.datetime(2018, 1, 1, 10, 10)
    assert as_datetime('  2018-01-01 10:10:00  ') == expected_datetime


def test_datetime_str():
    assert as_datetime_str('2018-01-01') == '2018-01-01'
