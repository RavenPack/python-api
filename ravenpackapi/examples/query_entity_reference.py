from ravenpackapi import RPApi

# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi()

# here we know a couple of RP_ENTITY_ID for 2 common entities
# we want to ask for all the known entity metadata
GOOGLE_RP_ENTITY_ID = '4A6F00'

references = api.get_entity_reference(GOOGLE_RP_ENTITY_ID)
print(references)
for name in references.names:
    print(name.value, name.start, name.end)

for ticker in references.tickers:
    if ticker.is_valid():
        print("Ticker:", ticker)
