import os

from ravenpackapi import RPApi

api = RPApi()

reference_filename = 'reference.csv'
if os.path.isfile(reference_filename):
    # use the locally saved reference file if it exists
    reference = api.get_entity_type_referen = api.get_entity_type_reference_from_file(reference_filename)
else:
    print("Retrieving the company mapping file")
    # get the latest reference file for all the COMP entities
    # call it without arguments to get all entities of all types
    reference = api.get_entity_type_reference('COMP')
    reference.write_to_file(reference_filename)

# with the reference we can also ask for a single entity given the ID
for rp_entity_id in ['4A6F00', '01F2E5']:  # add here as many as you want - they won't cause extra requests
    company = reference[rp_entity_id]
    valid_sedols = [sedol.value
                    for sedol in company.sedols
                    if sedol.is_valid()  # get all the sedol that are valid now
                    # (you can pass a date to is_valid to get the ones valid point-in-time
                    ]
    print(company.name, valid_sedols)
