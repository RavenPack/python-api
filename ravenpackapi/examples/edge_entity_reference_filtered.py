"""
Given a list of entities and a list of mapping metadata we are interested into
(e.g. SEDOL, TICKER, LISTING, etc) get all the mapping values for those entities
from the API and write them into a CSV.

NOTE: This script is meant specially for EDGE. RavenPack provides mapping files
ready for the user to download, for both RPA and EDGE, with the only drawback
that the files for EDGE are way bigger (in the order of GBs). This script helps
you get those mappings for the entities you are interested into, without having
to download all the rest.
"""

import csv

from ravenpackapi import RPApi

PRODUCT = "edge"
api = RPApi(product=PRODUCT)


COLUMN_NAMES = [
    "RP_ENTITY_ID",
    "ENTITY_TYPE",
    "DATA_TYPE",
    "DATA_VALUE",
    "RANGE_START",
    "RANGE_END",
]
DATA_TYPE_COLUMN = 2


def get_entity_references_as_list(entity_key, entity_type):
    """Call the API and get the mapping metadata for a given entity"""
    mapping_values = []
    reference = api.get_entity_reference(entity_key)
    for data_type, metadata in reference._data.items():
        if not isinstance(metadata, list):
            continue
        for m in metadata:
            mapping_values.append(
                [
                    entity_key,
                    entity_type,
                    data_type.upper(),
                    m["data_value"],
                    m.get("range_start"),
                    m.get("range_end"),
                ]
            )
    return mapping_values


def filter_mapping_values(mapping_values, data_types_to_filter):
    """
    Given the list of all the mapping metadata, filter the ones I am interested into
    """
    return [v for v in mapping_values if v[DATA_TYPE_COLUMN] in data_types_to_filter]


def print_mapping_values(mapping_values):
    """Print all the mapping values into the console"""
    print(",".join(COLUMN_NAMES))
    for m in mapping_values:
        vals = [v if v is not None else "" for v in m]
        print(",".join(vals))


def write_mapping_values(mapping_values, filename="edge-reference.csv"):
    """Write all the mapping values into a CSV"""
    with open(filename, "w") as f:
        csv_writer = csv.writer(f, delimiter=",")
        csv_writer.writerow(COLUMN_NAMES)
        for row in mapping_values:
            csv_writer.writerow(row)


def main():
    entities = [
        ("4A6F00", "COMP"),
        ("01F2E5", "COMP"),
    ]

    mapping_values = []
    for entity_key, entity_type in entities:
        mapping_values += get_entity_references_as_list(entity_key, entity_type)

    # Comment this line to not filter by data type
    mapping_values = filter_mapping_values(mapping_values, ["SEDOL"])

    print_mapping_values(mapping_values)
    write_mapping_values(mapping_values)


if __name__ == "__main__":
    main()
