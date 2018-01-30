from ravenpackapi import RPApi
from ravenpackapi.models.results import Results


class TestDatasetJson(object):
    api = RPApi()

    def test_known_swiss(self):
        ds = self.api.get_dataset(dataset_id='swiss20')
        data = ds.json(
            start_date='2018-01-01 18:00:00',
            end_date='2018-01-02 18:00:00',
        )
        assert isinstance(data, Results)
        assert len(data) > 500, 'We should have more data in 1 day of swiss20'
