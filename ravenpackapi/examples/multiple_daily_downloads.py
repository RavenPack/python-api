# an example of how to ask for a daily dump of multiple datasets, concurrently
import datetime
from typing import List

from ravenpackapi import Dataset, RPApi

api = RPApi(api_key="YOUR_API_KEY")
dataset_ids = [
    "DATASET_ID_1",
    "DATASET_ID_2",
    "DATASET_ID_3",
    # Write here all the datasets to download
]


def multiple_daily_download(dataset_ids: List):
    end_date = datetime.datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start_date = end_date - datetime.timedelta(days=1)
    start_date_str = start_date.strftime("%Y-%m-%d")
    print("Date range: %s-%s" % (start_date, end_date))
    print("Generating jobs")
    jobs = []
    for dataset_id in dataset_ids:
        dataset = Dataset(api=api, id=dataset_id)
        job = dataset.request_datafile(start_date, end_date)
        jobs.append((dataset_id, job))

    print("Waiting for the jobs to complete")
    for dataset_id, job in jobs:
        job.wait_for_completion()
        output_filename = f"dailydata-{dataset_id}-{start_date_str}.csv"
        job.save_to_file(output_filename)
        print("Daily download saved on:", output_filename)


if __name__ == "__main__":
    multiple_daily_download(dataset_ids)
