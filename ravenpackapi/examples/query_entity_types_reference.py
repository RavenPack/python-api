from ravenpackapi import RPApi

# initialize the API (here we use the RP_API_KEY in os.environ)
api = RPApi()

# get the latest reference file for all the TEAM entities
# call it without arguments to get all entities
team_reference = api.get_entity_type_reference('TEAM')

# we can then write this to file
team_reference.write_to_file('team_reference.csv')

# with the reference we can also ask for a single entity given the ID
team = team_reference['022568']
print(team.name)

# or iterate through them
for team in team_reference:
    print(team)
