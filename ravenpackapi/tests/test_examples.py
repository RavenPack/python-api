from ravenpackapi import RPApi, Dataset


class TestConditions(object):
    api = RPApi()
    ds = None

    @classmethod
    def setup_class(cls):
        cls.ds = cls.api.create_dataset(Dataset.from_dict(
            {
                "name": "Test custom dataset",
                "fields": [
                    "timestamp_utc",
                    "rp_entity_id",
                    "entity_name",
                    "AVG_REL"
                ],
                "filters": {
                    "relevance": {"$gte": 90}
                },
                "custom_fields": [
                    {
                        "AVG_REL": {
                            "avg": {
                                "field": "RELEVANCE",
                                "mode": "daily"
                            }
                        }
                    }
                ],
                "conditions": {
                    "$and": [
                        {
                            "AVG_REL": {
                                "$gt": 30
                            }
                        },
                        {
                            "rp_entity_id": {
                                "$in": [
                                    "ROLLUP"
                                ]
                            }
                        }
                    ]
                },
                "frequency": "daily",
                "tags": []
            }
        ))

    def test_dataset_copy_updated(self):
        source_dataset = Dataset(api=self.api, id='us30')
        new_dataset = Dataset(
            api=self.api,
            name="copy of the us30 dataset",
            filters=source_dataset.filters,
            fields=['timestamp_utc', 'rp_entity_id', 'avg_sentiment'],
            custom_fields=[{"avg_sentiment": {
                "avg": {
                    "field": "EVENT_SENTIMENT_SCORE",
                }
            }}],
            frequency='daily',
            tags=['copy', 'test']
        )
        new_dataset.save()
        new_dataset.delete()

    @classmethod
    def teardown_class(cls):
        cls.ds.delete()
