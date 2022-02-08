from ravenpackapi import RPApi, Dataset

api = RPApi(api_key="YOUR_API_KEY", product="edge")

ds = api.create_dataset(
    Dataset(
        **{
            "name": "Edge Dataset",
            "product": "edge",
            "product_version": "1.0",
            "frequency": "granular",
            "fields": [
                "timestamp_utc", "rp_document_id", "rp_entity_id", "entity_type", "entity_name",
                "country_code", "event_relevance", "entity_sentiment", "event_sentiment", "topic", "group",
                "title"
            ],
            "filters": {
                "$and": [
                    {"event_relevance": {"$gte": 90}},
                    {"country_code": {"$in": ["GB"]}},
                    {"event_sentiment": {"$nbetween": [-0.5, 0.5]}}
                ]
            },
        }
    )
)

print("Dataset created", ds)
