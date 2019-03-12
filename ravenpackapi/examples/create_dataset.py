from ravenpackapi import RPApi, Dataset

api = RPApi()

ds = api.create_dataset(
    Dataset(
        **{
            "product": "rpa",
            "product_version": "1.0",
            "name": "Events in UK - example",
            "fields": [
                "timestamp_utc",
                "rp_story_id",
                "rp_entity_id",
                "entity_type",
                "entity_name",
                "country_code",
                "relevance",
                "event_sentiment_score",
                "topic",
                "group",
                "headline"
            ],
            "filters": {
                "$and": [
                    {
                        "relevance": {
                            "$gte": 90
                        }
                    },
                    {
                        "country_code": {
                            "$in": [
                                "GB"
                            ]
                        }
                    },
                    {
                        "event_sentiment_score": {
                            "$nbetween": [-0.5, 0.5]
                        }
                    }
                ]
            },
            "frequency": "granular",
        }
    )
)

print("Dataset created", ds)
