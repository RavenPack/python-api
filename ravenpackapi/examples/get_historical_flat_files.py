# Download the historical compressed flat files (with all entities or just companies)
# they are decompressed and combined in a single csv file per year

import os
import zipfile

import requests

from ravenpackapi import RPApi
from ravenpackapi.util import parse_csv_line

api_key = os.environ['RP_API_KEY']  # set your API KEY here
api = RPApi(api_key)

flat_type = 'companies'  # can be 'companies' or 'full'
flat_list = api.get_flatfile_list(flat_type)
for flat_file in flat_list:
    local_filename = flat_file['name']
    output_filename = '%s.combined.csv' % local_filename
    if not os.path.isfile(output_filename):
        with open(output_filename, 'wb') as output:
            headers_written = False
            with requests.get(
                'https://app.ravenpack.com/history/getfile',
                dict(token=api_key, id=flat_file['id'], type=flat_type),
                stream=True,
            ) as flatzip:
                flatzip.raise_for_status()
                if not os.path.isfile(local_filename):
                    print("Downloading", local_filename, flat_file['size'])
                    with open(local_filename, 'wb') as f:
                        for chunk in flatzip.iter_content(chunk_size=8192):
                            f.write(chunk)
                with zipfile.ZipFile(local_filename) as zipped:
                    for fileinfo in zipped.namelist():
                        print(fileinfo)
                        with zipped.open(fileinfo) as csv:
                            header_line = next(csv)
                            headers = parse_csv_line(header_line)
                            if not headers_written:
                                output.write(header_line)
                                headers_written = True
                            for line in csv:
                                row = parse_csv_line(line)
                                output.write(line)
