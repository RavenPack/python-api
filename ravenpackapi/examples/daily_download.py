# an example of how to ask for a daily dump
import datetime

from ravenpackapi import RPApi, Dataset

api = RPApi(api_key='YOUR_API_KEY')
dataset_id = 'YOUR_DATASET_ID'


def daily_download(dataset_id):
    end_date = datetime.datetime.utcnow().replace(hour=0, minute=0,
                                                  second=0, microsecond=0)
    start_date = end_date - datetime.timedelta(days=1)
    print("Date range: %s-%s" % (start_date, end_date))
    dataset = Dataset(api=api, id=dataset_id)
    job = dataset.request_datafile(
        start_date, end_date
    )
    print("Waiting for the job to complete")
    job.wait_for_completion()
    output_filename = "dailydata-%s.csv" % start_date.strftime("%Y-%m-%d")
    job.save_to_file(output_filename)
    print("Daily download saved on:", output_filename)


if __name__ == '__main__':
    daily_download(dataset_id)
