import datetime
import os

from ravenpackapi import RPApi

PRODUCT = "rpa"  # Or PRODUCT = "edge"
api = RPApi(product=PRODUCT)


def download_or_read_reference_file(reference_filename="reference.csv"):
    if os.path.isfile(reference_filename):
        # use the locally saved reference file if it exists
        reference = api.get_entity_type_reference_from_file(reference_filename)
    else:
        print("Retrieving the company mapping file")
        # get the latest reference file for all the COMP entities
        # call it without arguments to get all entities of all types
        reference = api.get_entity_type_reference("COMP")
        reference.write_to_file(reference_filename)
    return reference


def get_valid_sedols(company, when=None):
    """Get all the sedol that are valid now (you can pass a date to is_valid to get the ones valid point-in-time"""
    return [sedol.value for sedol in company.sedols if sedol.is_valid(when)]


if __name__ == "__main__":
    # with the reference we can also ask for a single entity given the ID
    NOW = None
    entities = [
        ("4A6F00", NOW),
        ("01F2E5", datetime.date(2019, 1, 1)),
    ]
    if PRODUCT == "edge":
        # With Edge - the Reference-mapping are huge - so they're not kept in memory
        # you can either save them to file (about 2GB) and filter them or query
        # individual entities like this:
        reference = {
            entity_key: api.get_entity_reference(entity_key)
            for entity_key, date in entities
        }
    else:
        reference = download_or_read_reference_file()

    for (
        entity_key,
        when,
    ) in entities:
        company = reference[entity_key]
        valid_sedols = get_valid_sedols(company, when)
        print(company.name, valid_sedols)
