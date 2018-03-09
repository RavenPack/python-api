from ravenpackapi import RPApi, Dataset
import logging

logging.basicConfig(level=logging.INFO)
# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi()

# get the us30 dataset (its filters contain the top 30 US companies)
us30 = Dataset(api=api, id='us30')

print(us30.filters)

# creating a new dataset with modified filters and fields
# the filters are an aggregation of the us30 with some additional rule
new_filters = {"$and": [
    us30.filters,
    {"relevance": {
        "$gte": 90
    }
    },
    {
        "event_similarity_days": {
            "$gte": 1
        }
    }
]}
new_fields = [
    {
        "daily_average_ess_1d": {
            "avg": {
                "field": "EVENT_SENTIMENT_SCORE",
                "lookback": 1,
                "mode": "daily"
            }
        }
    },
    {
        "daily_average_ess_90d": {
            "avg": {
                "field": "EVENT_SENTIMENT_SCORE",
                "lookback": 90,
                "mode": "daily"
            }
        }
    },
    {
        "buzz": {
            "buzz": {
                "field": "RP_ENTITY_ID",
                "lookback": 2
            }
        }
    },
    {
        "news_count_1d": {
            "count": {
                "field": "RP_ENTITY_ID"
            }
        }
    },
    {
        "average_news_count_90d": {
            "avg": {
                "field": "news_count_1d",
                "lookback": 90
            }
        }
    }
]

custom_dataset = Dataset(api=api,
                         name="Us30 indicators",
                         filters=new_filters,
                         fields=new_fields,
                         frequency='daily'
                         )
custom_dataset.save()
print(custom_dataset)

# query the datafile and save it to file
job = custom_dataset.request_datafile(
    start_date='2017-01-01 19:30',
    end_date='2017-01-02 19:30',
    compressed=True,
    time_zone='Europe/London',
)

job.save_to_file('output.csv')
