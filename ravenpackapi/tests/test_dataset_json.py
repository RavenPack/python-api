from ravenpackapi import RPApi, Dataset
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

    def test_indicator_dataset(self):
        indicator_dataset = Dataset(
            name='Test-indicator-dataset',
            filters={"$and": [{"rp_entity_id": {"$in": ["D8442A"]}}]},
            fields=[{"average": {"avg": {"field": "EVENT_SENTIMENT_SCORE"}}}],
            frequency='daily',
        )
        indicator_dataset = self.api.create_dataset(indicator_dataset)
        try:

            # ask the indicator dataset for its data
            response = indicator_dataset.json('2018-01-01 00:00', '2018-01-02 00:00')
            assert len(response) == 2  # we should get 2 rows
            assert {r['rp_entity_id'] for r in response} == {'D8442A', 'ROLLUP'}

            # do a request overriding fields and frequency to see the underlying data
            response = indicator_dataset.json('2018-01-01 00:00', '2018-01-02 00:00',
                                              fields=['rp_story_id', 'rp_entity_id'],
                                              frequency='granular')
            assert len(response) > 200, "We should have many granular analytics rows"
            assert {r['rp_entity_id'] for r in response} == {'D8442A'}, "All rows should be D8442A"
        finally:
            indicator_dataset.delete()

    def test_granular_dataset(self):
        self.api.log_curl_commands = True
        granular_dataset = Dataset(
            name='Test-granular-dataset',
            filters={"$and": [{"rp_entity_id": {"$in": ["D8442A"]}}, {"relevance": 90}]},
        )
        granular_dataset = self.api.create_dataset(granular_dataset)
        try:
            granular_dataset.json('2018-01-01 00:00', '2018-01-02 00:00')
        finally:
            granular_dataset.delete()
