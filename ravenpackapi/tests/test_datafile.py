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
