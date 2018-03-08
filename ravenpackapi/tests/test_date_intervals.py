import datetime

from ravenpackapi.util import time_intervals, SPLIT_YEARLY, SPLIT_MONTHLY


class TestTimeRanges(object):
    def test_monthly_ranges(self):
        start = datetime.datetime(2017, 11, 2)
        end = datetime.datetime(2018, 3, 15)

        intervals = [tuple(map(lambda d: d.strftime("%Y-%m-%d"), rng))
                     for rng in time_intervals(start, end)]
        assert intervals == [
            ('2017-11-02', '2017-12-01'),
            ('2017-12-01', '2018-01-01'),
            ('2018-01-01', '2018-02-01'),
            ('2018-02-01', '2018-03-01'),
            ('2018-03-01', '2018-03-15')
        ]

    def test_yearly_ranges(self):
        start = datetime.datetime(2015, 11, 2)
        end = datetime.datetime(2018, 3, 15)

        intervals = [tuple(map(lambda d: d.strftime("%Y-%m-%d"), rng))
                     for rng in time_intervals(start, end,
                                               split=SPLIT_YEARLY)]
        assert intervals == [
            ('2015-11-02', '2016-01-01'),
            ('2016-01-01', '2017-01-01'),
            ('2017-01-01', '2018-01-01'),
            ('2018-01-01', '2018-03-15')
        ]

    def test_with_string_inputs(self):
        start = '2015-11-30'
        end = '2016-01-10 11:30'
        intervals = [tuple(map(lambda d: d.strftime("%Y-%m-%d %H:%M"), rng))
                     for rng in time_intervals(start, end,
                                               split=SPLIT_YEARLY)]
        assert intervals == [
            ('2015-11-30 00:00', '2016-01-01 00:00'),
            ('2016-01-01 00:00', '2016-01-10 11:30'),
        ]

    def test_minutes_months(self):
        start = '2015-11-30 15:00'
        end = '2016-01-10 11:30'
        intervals = [tuple(map(lambda d: d.strftime("%Y-%m-%d %H:%M"), rng))
                     for rng in time_intervals(start, end,
                                               split=SPLIT_MONTHLY)]
        assert intervals == [
            ('2015-11-30 15:00', '2015-12-01 00:00'),
            ('2015-12-01 00:00', '2016-01-01 00:00'),
            ('2016-01-01 00:00', '2016-01-10 11:30'),
        ]

    def test_minutes_years(self):
        start = '2015-11-30 15:00'
        end = '2016-01-10 11:30'
        intervals = [tuple(map(lambda d: d.strftime("%Y-%m-%d %H:%M"), rng))
                     for rng in time_intervals(start, end,
                                               split=SPLIT_YEARLY)]
        assert intervals == [
            ('2015-11-30 15:00', '2016-01-01 00:00'),
            ('2016-01-01 00:00', '2016-01-10 11:30'),
        ]

    def test_very_short_interval(self):
        start = '2004-02-29 15:00'
        end = '2004-02-29 16:00'
        intervals = [tuple(map(lambda d: d.strftime("%Y-%m-%d %H:%M"), rng))
                     for rng in time_intervals(start, end,
                                               split=SPLIT_YEARLY)]
        assert intervals == [
            (start, end),
        ]
