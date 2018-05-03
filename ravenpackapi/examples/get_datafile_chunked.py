"""

Download all data from the chosen dataset in a time range
Download files are compressed, and chunked per year

"""

import os

from ravenpackapi import RPApi
from ravenpackapi.util import time_intervals, SPLIT_WEEKLY

api = RPApi(api_key='YOUR_API_KEY')
ds = api.get_dataset('YOUR_DATASET_ID')

start_date = '2018-01-01'
end_date = '2018-01-10'
GET_COMPRESSED = True

output_folder = './output'

os.makedirs(output_folder, exist_ok=True)  # create folder for output
for range_start, range_end in time_intervals(start_date, end_date,
                                             split=SPLIT_WEEKLY,
                                             # available splits:
                                             # SPLIT_YEARLY, SPLIT_WEEKLY, SPLIT_DAILY
                                             # or SPLIT_MONTHLY (the default)
                                             ):
    job = ds.request_datafile(
        start_date=range_start,
        end_date=range_end,
        compressed=GET_COMPRESSED,
    )
    if job is None:
        print("There is no data in the range", range_start, range_end)
        continue
    filename = os.path.join(output_folder,
                            "datafile-{datestr}.{ext}".format(
                                datestr=range_start.strftime('%Y-%m-%d'),
                                ext='zip' if GET_COMPRESSED else 'csv')
                            )
    print("Saving", range_start, "-", range_end, "=>", filename)
    with open(filename, 'wb') as fp:
        job.save_to_file(filename=fp.name)
