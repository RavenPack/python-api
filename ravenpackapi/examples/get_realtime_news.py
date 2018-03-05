import logging

from ravenpackapi import RPApi

logging.basicConfig(level=logging.DEBUG)
# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi()

# query the realtime feed
ds = api.get_dataset(dataset_id='us500')

for record in ds.request_realtime():
    print(record)
    print(record.timestamp_utc, record.entity_name,
          record['event_relevance'])
