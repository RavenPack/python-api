#!/usr/bin/env python
from __future__ import print_function

import argparse
import datetime
import threading

from ravenpackapi import RPApi
from ravenpackapi.models.results import Result

# import logging
# logging.basicConfig(level=logging.DEBUG) # show all the API calls

parser = argparse.ArgumentParser(description="RavenPack API connection check",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--key', type=str,
                    help='RavenPack API KEY')


def check_datafile():
    print('Datafile ...')
    job = ds.request_datafile(
        start_date=date_start,
        end_date=date_end,
        fields=['rp_story_id', 'timestamp_utc']
    )
    records = []
    for record in job.iterate_results(include_headers=True):
        records.append(record)
    assert len(records) > 1
    assert records[0] == ['RP_STORY_ID', 'TIMESTAMP_UTC']  # we want the headers
    print('Datafile - OK')
    results['datafile'] = True


def check_json():
    print('JSON ...')

    records = ds.json(
        start_date=date_start,
        end_date=date_end,
        fields=['rp_story_id', 'timestamp_utc']
    )
    assert len(records) > 1
    print('JSON - OK')
    results['json'] = True


def check_realtime():
    print("Realtime ...")
    for record in ds.request_realtime():
        assert isinstance(record, Result)
        break
    print('Realtime - OK')
    results['realtime'] = True


if __name__ == '__main__':
    args = parser.parse_args()
    api = RPApi(args.key)

    ds = api.get_dataset('all-granular-data')
    date_end = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
    date_start = date_end - datetime.timedelta(minutes=3)  # 3 minutes of data

    if not api.api_key:
        print("Please provide an APIKEY: with the --key parameter or setting the RP_API_KEY environment variable")
        exit(1)
    print("Checking connection with APIKEY: %s" % api.api_key)

    checks = [
        threading.Thread(target=check_datafile),
        threading.Thread(target=check_json),
        threading.Thread(target=check_realtime),
    ]
    results = dict(
        datafile=False,
        json=False,
        realtime=False,
    )
    for job in checks:
        job.start()
    print()

    for job in checks:
        job.join(timeout=120)
    print()

    print("Connection check:")
    for k, v in results.items():
        print("%10s: %s" % (k, v))
    if not all(results.values()):
        print("Connection check FAILED!")
        exit(1)
    else:
        print("Connection check SUCCEEDED")
