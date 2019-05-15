import logging

from ravenpackapi import RPApi, Dataset

logging.basicConfig(level=logging.INFO)
# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi()

dataset_id = None  # put here a dataset_id if you have it already

if dataset_id is None:
    dataset = Dataset(
        api=api,
        filters={},
        name='Average sentiment',
        frequency='daily',
        fields=[{'average_ess': {'avg': {'field': 'EVENT_SENTIMENT_SCORE'}}}]
    )
    dataset_id = dataset.save()
else:
    dataset = api.get_dataset(dataset_id)

# job = Job(api=api,
#           token='xxx')  # if you already have a job you can use this

# ... or request a new one
job = dataset.request_datafile(
    start_date='2018-01-01 00:00:00',
    end_date='2018-01-02 00:00:00',
)

# write only the ROLLUP rows
for line in job.iterate_results():
    timestamp, entity_id, entity_name, avg_sentiment = line
    if entity_id == 'ROLLUP':
        print(line)
