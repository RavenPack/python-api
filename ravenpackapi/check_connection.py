#!/usr/bin/env python
import argparse
import datetime
import threading

from ravenpackapi import RPApi
from ravenpackapi.exceptions import APIException
from ravenpackapi.models.results import Result

# import logging
# logging.basicConfig(level=logging.DEBUG) # show all the API calls

ALL_GRANULAR_DATA = "all-granular-data"
US_500_EDGE = "us500-edge"


class ConnectionChecker:
    def __init__(self, api_key, dataset_id, product):
        self.product = product
        self.api = RPApi(api_key, product)
        self.dataset_id = dataset_id
        self._dataset = None
        if not self.api.api_key:
            print(
                "Please provide an APIKEY: with the --key parameter or setting the RP_API_KEY environment variable"
            )
            exit(1)
        self.date_end = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
        self.date_start = self.date_end - datetime.timedelta(
            minutes=1
        )  # 1 minute of data

    @property
    def dataset(self):
        if self._dataset is None:
            self._dataset = self.api.get_dataset(self.dataset_id)
        return self._dataset

    def user_has_product(self):
        try:
            datasets = self.api.list_datasets()
        except APIException as e:
            if e.response.status_code in [400, 403]:
                # User has no access to product
                return False
            raise
        return True

    def check_datafile(self):
        job = self.dataset.request_datafile(
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
        records = self.dataset.json(
            start_date=self.date_start,
            end_date=self.date_end,
            fields=[self.rp_story_id, "timestamp_utc"],
            frequency="granular",
        )
        assert len(records) > 1
        self.results["json"] = True

    def check_realtime(self):
        for record in self.dataset.request_realtime():
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

    valid_checkers = []
    for checker in checkers:
        if not checker.user_has_product():
            print("-" * 35)
            print(f"[{checker.product.upper()}] No access. Skipping checks.")
        else:
            valid_checkers.append(checker)

    for checker in valid_checkers:
        checker.check_all()

    for checker in valid_checkers:
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
        ConnectionChecker(args.key, US_500_EDGE, "edge"),
    )


if __name__ == "__main__":
    main()
