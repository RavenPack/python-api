# an example of how to ask for a daily, weekly or monthly dump
import datetime

from ravenpackapi import Dataset, RPApi

api = RPApi(api_key="YOUR_API_KEY")
dataset_id = "YOUR_DATASET_ID"


def daily_download(dataset_id):
    end_date = datetime.datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start_date = end_date - datetime.timedelta(days=1)
    print("Date range: %s-%s" % (start_date, end_date))
    dataset = Dataset(api=api, id=dataset_id)
    job = dataset.request_datafile(start_date, end_date)
    print("Waiting for the job to complete")
    job.wait_for_completion()
    output_filename = "dailydata-%s.csv" % start_date.strftime("%Y-%m-%d")
    job.save_to_file(output_filename)
    print("Daily download saved on:", output_filename)


def weekly_download(dataset_id):
    today = datetime.datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_date = today - datetime.timedelta(days=today.weekday())
    start_date = end_date - datetime.timedelta(days=7)
    print("Date range: %s-%s" % (start_date, end_date))
    dataset = Dataset(api=api, id=dataset_id)
    job = dataset.request_datafile(start_date, end_date)
    print("Waiting for the job to complete")
    job.wait_for_completion()
    output_filename = "weeklydata-%s.csv" % start_date.strftime("%Y-%m-%d")
    job.save_to_file(output_filename)
    print("Weekly download saved on:", output_filename)


def monthly_download(dataset_id):
    today = datetime.datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_date = datetime.datetime(today.year, today.month, 1)
    if today.month == 1:
        start_date = datetime.datetime(today.year - 1, 12, 1)
    else:
        start_date = datetime.datetime(today.year, today.month - 1, 1)
    print("Date range: %s-%s" % (start_date, end_date))
    dataset = Dataset(api=api, id=dataset_id)
    job = dataset.request_datafile(start_date, end_date)
    print("Waiting for the job to complete")
    job.wait_for_completion()
    output_filename = "monthlydata-%s.csv" % start_date.strftime("%Y-%m-%d")
    job.save_to_file(output_filename)
    print("Monthly download saved on:", output_filename)


if __name__ == "__main__":
    daily_download(dataset_id)
    weekly_download(dataset_id)
    monthly_download(dataset_id)
