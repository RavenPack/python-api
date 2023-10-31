from ravenpackapi import Dataset, RPApi
from ravenpackapi.exceptions import APIException404

DATASET_ID = "THE_ID_OF_THE_DATASET_TO_DOWNLOAD"


def main():
    api = RPApi()
    ds = Dataset(api=api, id=DATASET_ID)

    try:
        do_delete = input(f"Are you sure you want to delete the {ds}? (y/N)")
        if do_delete.upper() == "Y":
            ds.delete()
            print("Deleted", ds)
    except APIException404:
        print("Can't delete dataset because it was not found")


if __name__ == "__main__":
    main()
