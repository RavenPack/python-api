"""
Example that lists jobs (processing, completed or in error) that have been
updated in a time range, and prints them.
"""

import datetime

from ravenpackapi import RPApi

# initialize the API (here we use the RP_API_KEY in os.environ)
PRODUCT = "rpa"  # Or PRODUCT = "edge"
api = RPApi(product=PRODUCT)


def print_jobs(jobs):
    for job in jobs:
        print_job(job)


def print_job(job):
    status = "failed" if job.status == "error" else job.status
    start, end = [job._data[date] for date in ("start_date", "end_date")]
    id = job.token
    print(f"Job {status} with ID {id} with data ranging from {start} to {end}")


if __name__ == "__main__":
    # Define start_date and end_date or use the current date
    # start = "2022-11-22"
    # end = "2022-11-23"
    DAYS_BACK = 1
    end = datetime.datetime.utcnow().replace(microsecond=0)
    start = end - datetime.timedelta(days=DAYS_BACK)

    # Print all finished_jobs: completed or in error
    finished_jobs = api.list_jobs(start, end, status=["completed", "error"])
    print(f"{len(finished_jobs)} jobs completed or in error between {start} and {end}:")
    print_jobs(finished_jobs)

    # Print running jobs
    jobs = api.list_jobs(start, end, status=["processing"])
    print(f"{len(jobs)} jobs processing between {start} and {end}:")
    print_jobs(jobs)
