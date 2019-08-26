# Download the historical compressed flat files (with all entities or just companies)
# they are decompressed and combined into a single csv file per year

import os
import zipfile

from ravenpackapi import RPApi
from ravenpackapi.util import parse_csv_line

api_key = os.environ['RP_API_KEY']  # set your API KEY here
api = RPApi(api_key)

flat_type = 'companies'  # can be 'companies' or 'full'
flat_list = api.get_flatfile_list(flat_type)
for flat_file in flat_list:
    file_id = flat_file['id']
    combined_year_filename = '%s.combined.csv' % file_id
    if not os.path.isfile(combined_year_filename):
        with open(combined_year_filename, 'wb') as output:
            headers_written = False
            with api.get_flatfile(flat_type, file_id) as flatzip:
                if not os.path.isfile(file_id):
                    print("Downloading", file_id, flat_file['size'] / 1024 / 1024, "MB")
                    with open(file_id, 'wb') as f:
                        for chunk in flatzip.iter_content(chunk_size=8192):
                            f.write(chunk)
                with zipfile.ZipFile(file_id) as zipped:
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
