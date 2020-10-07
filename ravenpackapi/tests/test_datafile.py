import tempfile

import pytest

from ravenpackapi import RPApi
from ravenpackapi.models.job import Job


class TestDatafile(object):
    api = RPApi()

    @pytest.mark.slow
    @pytest.mark.datafile
    def test_small_async_download(self):
        ds = self.api.get_dataset(dataset_id='swiss20')
        job = ds.request_datafile(
            start_date='2018-01-01 18:00:00',
            end_date='2018-01-02 18:00:00',
        )
        assert isinstance(job, Job)
        with tempfile.NamedTemporaryFile() as fp:
            job.save_to_file(filename=fp.name)

    @pytest.mark.slow
    @pytest.mark.datafile
    def test_small_async_with_headers(self):
        ds = self.api.get_dataset(dataset_id='swiss20')
        job = ds.request_datafile(
            start_date='2018-01-01 18:00:00',
            end_date='2018-01-01 18:05:00',
            fields=['rp_story_id', 'timestamp_utc']
        )
        records = []
        for record in job.iterate_results(include_headers=True):
            records.append(record)
        assert len(records) > 1
        assert records[0] == ['RP_STORY_ID', 'TIMESTAMP_UTC']  # we want the headers

    def test_job_list_in_error(self):
        start_date = '2018-01-01',
        end_date = '2018-02-01 00:00:00',
        jobs = self.api.list_jobs(start_date, end_date)
        assert isinstance(jobs, list)

    def test_job_list_completed(self):
        start_date = '2018-01-01',
        end_date = '2018-02-01 00:00:00',
        jobs = self.api.list_jobs(start_date, end_date, status=['COMPLETED'])
        assert isinstance(jobs, list)
