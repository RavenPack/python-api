from ravenpackapi import RPApi
import logging

logging.basicConfig(level=logging.DEBUG)
# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi()

# query the json endpoint for a dataset ***
# use the public dataset with id 'us30'
ds = api.get_dataset(dataset_id='us30')
# query the dataset analytics with the json endpoint
print(ds)

data = ds.json(
    start_date='2018-01-05 18:00:00',
    end_date='2018-01-05 18:01:00',
)

for record in data:
    print(record)

# query the ad-hoc json endpoint ***
adhoc_data = api.json(
    start_date='2018-01-05 18:00:00',
    end_date='2018-01-05 18:01:00',
    fields=ds.fields,
    filters=ds.filters,
)
print(adhoc_data)
for record in adhoc_data:
    print(record)
