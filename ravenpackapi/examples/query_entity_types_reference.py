from ravenpackapi import RPApi

# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi()
# With Edge - the Reference-mapping are huge - so they're not kept in memory
# you can either save them to file and filter them or query individual entities
# like in the query_entity_reference.py example

# get the latest reference file for all the TEAM entities
# call it without arguments to get all entities
team_reference = api.get_entity_type_reference("TEAM")

# we can then write this to file
team_reference.write_to_file("team_reference.csv")

# with the reference we can also ask for a single entity given the ID
team = team_reference["022568"]  # this won't work in Edge
print(team.name)

# or iterate through them
for team in team_reference:
    print(team)
