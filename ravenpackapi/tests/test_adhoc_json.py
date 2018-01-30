from ravenpackapi import RPApi
from ravenpackapi.models.results import Results


class TestAdHocJson(object):
    api = RPApi()

    def test_small_adhoc(self):
        data = self.api.json(
            start_date='2018-01-01 18:00:00',
            end_date='2018-01-01 18:05:00',
            fields=['timestamp_utc', 'rp_entity_id', 'headline'],
            filters={
                "entity_type": {"$in": ['PROD']},
                # "entity_type": "PROD",
            }
        )
        assert isinstance(data, Results)
        assert len(data) > 0, 'We should have some product in those 5 minutes'
