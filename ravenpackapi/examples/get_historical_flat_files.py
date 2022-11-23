# Download the historical compressed flat files (with all entities or just companies)
# they are decompressed and combined into a single csv file per year

import os
import zipfile

from ravenpackapi import RPApi
from ravenpackapi.util import parse_csv_line

PRODUCT = "rpa"  # Or PRODUCT="edge"

if PRODUCT == "rpa":
    # Flat type for RPA:
    FLAT_TYPE = "companies"  # One of "companies", "full"
    # FLAT_TYPE = "full"
else:
    # Flat type for EDGE:
    FLAT_TYPE = "ESS_POSITIVE"  # One of the many edge flatfiles


def main():
    api = RPApi(product=PRODUCT)

    flat_list = api.get_flatfile_list(FLAT_TYPE)

    for flat_file in flat_list:
        file_id = flat_file["id"]
        combined_year_filename = "%s.combined.csv" % file_id
        if os.path.isfile(combined_year_filename):
            continue
        download_flatfile(api, FLAT_TYPE, flat_file)
        unzip_to_csv(file_id, combined_year_filename)


def unzip_to_csv(zipname: str, csvname: str):
    with open(csvname, "wb") as output:
        with zipfile.ZipFile(zipname) as zf:
            for line in get_all_csv_lines_in_zip(zf):
                headers = parse_csv_line(line)
                output.write(line)


def get_all_csv_lines_in_zip(zf: zipfile.ZipFile):
    headers_written = False
    for fileinfo in zf.namelist():
        print(fileinfo)
        with zf.open(fileinfo) as csv:
            header_line = next(csv)
            if not headers_written:
                yield header_line
                headers_written = True
            for line in csv:
                yield line


def download_flatfile(
    api: RPApi, flat_type: str, flat_file: dict, chunk_size: int = 8192
):
    filename = flat_file["id"]
    flatsize = flat_file["size"]
    if os.path.isfile(filename):
        return False
    with api.get_flatfile(flat_type, filename) as flatzip:
        print("Downloading", filename, bytes_to_mbytes(flatsize), "MB")
        with open(filename, "wb") as f:
            for chunk in flatzip.iter_content(chunk_size=chunk_size):
                f.write(chunk)
    return True


def bytes_to_mbytes(b: int):
    return b / 1024 / 1024


if __name__ == "__main__":
    main()
