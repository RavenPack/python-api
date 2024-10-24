import pandas as pd

from ravenpackapi import RPApi

api = RPApi()

DATASET_ID = "YOUR_DATASET_ID"
CSV_FILE = "universe.csv"


def get_entity_ids(csv_file):
    """
    Reads a CSV file and returns the unique values of the column "rp_entity_id"
    """
    df = pd.read_csv(csv_file)
    return list(df["rp_entity_id"].unique())


def update_dataset(dataset_id, entity_ids):
    """
    Updates the filters in the dataset to match the list of entity_ids
    """
    dataset = api.get_dataset(dataset_id)
    dataset.filters = {"rp_entity_id": {"$in": entity_ids}}
    dataset.save()


def main():
    entity_ids = get_entity_ids(CSV_FILE)
    update_dataset(DATASET_ID, entity_ids)


if __name__ == "__main__":
    main()
