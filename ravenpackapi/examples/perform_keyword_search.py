import logging

from ravenpackapi import Dataset, RPApi

logging.basicConfig(level=logging.INFO)

PRODUCT = "rpa"  # Or PRODUCT = "edge"
api = RPApi(product=PRODUCT)

KEYWORDS = ["Script", "Python"]

START_DATE = "2023-02-01"
END_DATE = "2023-02-02"

HEADLINE = "title" if PRODUCT == "edge" else "headline"


def search_keyword(keyword, big=True):
    """
    Creates a dataset to search for a keyword.
    Downloads the data using the /datafile endpoint if big is True,
    or prints the results from the /json enpoint if big is False.
    Note: big=False may fail when results are too big.
    """
    ds = api.create_dataset(
        Dataset(
            **{
                "product": PRODUCT,
                "product_version": "1.0",
                "name": f"Keywords Search {keyword}",
                "tags": [],
                "filters": {
                    "$and": [
                        {HEADLINE: {"$search": [f'"{keyword}"']}},
                        {"document": {"$search": f'"{keyword}"'}},
                    ]
                },
                "frequency": "granular",
            }
        )
    )

    print("Date range: %s-%s" % (START_DATE, END_DATE))
    if big:
        # query the dataset analytics with the datafile endpoint
        job = ds.request_datafile(START_DATE, END_DATE)
        if job is None:
            print(f"\n\n-- NO DATA FOR KEYWORD '{keyword}' --")
            return

        print("Waiting for the job to complete")
        job.wait_for_completion()
        output_filename = f"dataset_keyword_search_{keyword}.csv"
        job.save_to_file(output_filename)
        print("Daily download saved on:", output_filename)
    else:
        # query the dataset analytics with the json endpoint for smaller results
        data = ds.json(
            start_date=START_DATE,
            end_date=END_DATE,
        )
        if not data:
            print(f"\n\n-- NO DATA FOR KEYWORD '{keyword}' --")
            return
        print(f"\n\n-- DATA FOR KEYWORD '{keyword}' --")

        for record in data:
            print(record)


def main():
    for keyword in KEYWORDS:
        search_keyword(keyword, big=True)


if __name__ == "__main__":
    main()
