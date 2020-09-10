from ravenpackapi import RPApi

from ravenpackapi.exceptions import APIException

# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi()

# query the json endpoint for a dataset ***
# use the public dataset with id 'us30'
ds = api.get_dataset(dataset_id='us30')

data = ds.json(
    start_date='2019-08-05 18:00:00',
    end_date='2019-08-05 18:01:00',
)

last_rp_story_id = None
for record in list(data)[:5]:  # get url of the first documents
    rp_story_id = record['rp_story_id']
    if last_rp_story_id is None or last_rp_story_id != rp_story_id:
        try:
            url = api.get_document_url(rp_story_id)
        except APIException as e:
            if e.response.status_code == 404:  # when the document is found, handle it gracefully
                url = None
            else:
                raise
        last_rp_story_id = rp_story_id
    print(rp_story_id,
          record['headline'],
          url,
          )
