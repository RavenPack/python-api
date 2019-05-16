import pytest

from ravenpackapi import RPApi


class TestDatasetCount(object):
    api = RPApi()

    @pytest.mark.json
    def test_count_timezone(self):
        ds = self.api.get_dataset(dataset_id='us30')
        count_results_utc = ds.count(
            start_date="2019-05-14",
            end_date="2019-05-15",
        )
        assert isinstance(count_results_utc, dict)

        count_results_london = ds.count(
            start_date="2019-05-14",
            end_date="2019-05-15",
            time_zone="Europe/London"
        )
        assert isinstance(count_results_london, dict)

        assert count_results_london != count_results_utc
