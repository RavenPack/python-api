#!/usr/bin/env python
from __future__ import print_function

import argparse
import datetime
import threading

from ravenpackapi import RPApi
from ravenpackapi.models.results import Result

# import logging
# logging.basicConfig(level=logging.DEBUG) # show all the API calls

ALL_GRANULAR_DATA = "all-granular-data"
NEWS_COMP = "0560FE1D2B70723364AF113465FD4673"


class ConnectionChecker:
    def __init__(self, api_key, dataset_id, product):
        self.product = product
        self.api = RPApi(api_key, product)
        if not self.api.api_key:
            print(
                "Please provide an APIKEY: with the --key parameter or setting the RP_API_KEY environment variable"
            )
            exit(1)
        self.ds = self.api.get_dataset(dataset_id)
        self.date_end = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
        self.date_start = self.date_end - datetime.timedelta(
            minutes=1
        )  # 1 minute of data

    def check_datafile(self):
        job = self.ds.request_datafile(
            start_date=self.date_start,
            end_date=self.date_end,
            fields=None,
        )
        records = []
        for record in job.iterate_results(include_headers=True):
            records.append(record)
        assert len(records) > 1
        # Check some headers
        assert self.rp_story_id.upper() in records[0]
        assert "TIMESTAMP_UTC" in records[0]

        self.results["datafile"] = True

    @property
    def rp_story_id(self):
        if self.product == "edge":
            return "rp_document_id"
        else:
            return "rp_story_id"

    def check_json(self):
        records = self.ds.json(
            start_date=self.date_start,
            end_date=self.date_end,
            fields=[self.rp_story_id, "timestamp_utc"],
            frequency="granular",
        )
        assert len(records) > 1
        self.results["json"] = True

    def check_realtime(self):
        for record in self.ds.request_realtime():
            assert isinstance(record, Result)
            break
        self.results["realtime"] = True

    def check_all(self):
        self.jobs = [
            threading.Thread(target=self.check_datafile),
            threading.Thread(target=self.check_json),
            threading.Thread(target=self.check_realtime),
        ]
        self.results = dict(
            datafile=False,
            json=False,
            realtime=False,
        )
        for job in self.jobs:
            job.start()

    def print_results(self):
        for job in self.jobs:
            job.join(timeout=120)
        print("-" * 35)
        print(f"[{self.product.upper()}] Connection check:")
        all_ok = True
        for check, ok in self.results.items():
            result = "OK" if ok else "ERROR"
            print("%10s: %s" % (check, result))
            if not ok:
                all_ok = False

        if all_ok:
            print(f"[{self.product.upper()}] Connection check SUCCEEDED")
        else:
            print(f"[{self.product.upper()}] Connection check FAILED!")


def run_checks(*checkers):
    print(f"Checking connection with APIKEY: {checkers[0].api.api_key} ...")
    print("This may take a few minutes")
    for checker in checkers:
        checker.check_all()

    for checker in checkers:
        checker.print_results()


def main():
    parser = argparse.ArgumentParser(
        description="RavenPack API connection check",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--key", type=str, help="RavenPack API KEY")

    args = parser.parse_args()
    run_checks(
        ConnectionChecker(args.key, ALL_GRANULAR_DATA, "rpa"),
        ConnectionChecker(args.key, NEWS_COMP, "edge"),
    )


if __name__ == "__main__":
    main()
