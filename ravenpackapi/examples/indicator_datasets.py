from ravenpackapi import RPApi, Dataset
from ravenpackapi.utils.helpers import delete_all_datasets_by_name

api = RPApi()

# Begin creating a dataset with your desired filters (see the RPA user guide for syntax)
# You can then add functions (https://app.ravenpack.com/api-documentation/#indicator-syntax)
# Alternatively you can also create the dataset via the query builder and just use the dataset_uuid
print("Creating a dataset with a few functions...")
dataset = Dataset(api,
                  name='My Indicator dataset',
                  filters={"relevance": {"$gt": 90}},
                  frequency='daily',
                  fields=[{"avg_1d": {"avg": {"field": "EVENT_SENTIMENT_SCORE", "lookback": 1,
                                              "mode": "granular"}}},
                          {"avg_7d": {
                              "avg": {"field": "avg_1d", "lookback": 1, "mode": "granular"}}},
                          {"buzz_365d": {"buzz": {"field": "RP_ENTITY_ID", "lookback": 365}}},
                          {"newsvolume_1d": {"count": {"field": "RP_ENTITY_ID", "lookback": 1}}},
                          {"newsvolume_365d": {"avg": {"field": "newsvolume_1d", "lookback": 365,
                                                       "mode": "granular"}}}]
                  )
dataset.save()

# you can also change the fields, (remember to save afterward)
print("Updating fields...")
dataset.fields = [
    {"avg": {"avg": {"field": "EVENT_SENTIMENT_SCORE", "lookback": 365}}},
]
dataset.save()

# Following this, you can then generate a datafile (for your desired date range)
print("Requesting a datafile in the CSV format...")
job = dataset.request_datafile(
    start_date='2018-04-10', end_date='2018-04-11',
    output_format='csv'
)
job.save_to_file('output.csv')  # This will poll until the file is ready for download
print("Saved to output.csv")

# a convenience function to delete all the dataset given a name
# delete_all_datasets_by_name(api, 'My Indicator dataset')

# here's an example of another dataset with custom_fields and conditions
print("Creating a new dataset with functions and conditions...")
dataset = api.create_dataset(Dataset.from_dict(
    {
        "name": "Dataset with functions and conditions",
        "fields": [
            "timestamp_utc",
            "rp_entity_id",
            "entity_name",
            "AVG_REL"
        ],
        "filters": {
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

dataset.save()
print("Dataset created:", dataset.id)
