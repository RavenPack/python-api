from ravenpackapi import RPApi

# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi()

for job in api.list_jobs('2020-01-01', '2020-10-10', status=['COMPLETED']):
    print(job)
