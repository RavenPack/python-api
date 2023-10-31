# anf how to get the top 3 event groups for a day based on volume
import csv
import datetime
import os.path

from ravenpackapi import Dataset, RPApi

DATASET_ID = "all-granular-data-edge"
PRODUCT = "edge"  # Or PRODUCT = "rpa"
api = RPApi(product=PRODUCT)


def get_today_range():
    end_date = datetime.datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start_date = end_date - datetime.timedelta(days=1)
    return start_date, end_date


def download_all_granular_data(dataset_id):
    start_date, end_date = get_today_range()
    yesterday = start_date.strftime("%Y-%m-%d")
    print("Date range: %s-%s" % (start_date, end_date))
    output_filename = f"{DATASET_ID}-{yesterday}.csv"

    if os.path.exists(output_filename):
        print(f"Datafile {output_filename} already exists")
    else:
        print(f"Datafile {output_filename} doesn't exist. Creating")
        dataset = Dataset(api=api, id=dataset_id)
        job = dataset.request_datafile(start_date, end_date)
        print("Waiting for the job to complete")
        job.wait_for_completion()
        job.save_to_file(output_filename)
        print("Daily download saved on:", output_filename)
    return output_filename


def get_all_event_groups(filename):
    with open(filename, newline="") as csvfile:
        rows = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        for row in rows:
            group = row["GROUP"]
            if group:
                yield group


def count_event_groups(all_event_groups):
    group_count = {}
    for group in all_event_groups:
        if group not in group_count:
            group_count[group] = 0
        group_count[group] += 1
    return list(sorted(group_count.items(), key=lambda item: item[1], reverse=True))


def main():
    filename = download_all_granular_data(DATASET_ID)
    all_event_groups = get_all_event_groups(filename)
    event_groups_sorted = count_event_groups(all_event_groups)
    print("Event groups read. Getting the top 5:")
    for group, count in event_groups_sorted[:5]:
        print(f"- {group}:\t{count}")


if __name__ == "__main__":
    main()
