import logging

import pytest

from ravenpackapi import RPApi, Dataset
from ravenpackapi.exceptions import JobNotProcessing, APIException

logger = logging.getLogger(__name__)


class TestJobCancellation(object):
    api = RPApi()
    ds = None

    @classmethod
    def setup_class(cls):
        cls.ds = cls.api.create_dataset(
            Dataset(
                name='test_job_cancel',
                filters={
                    "rp_entity_id": 'D8442A'
                },
            )
        )

    def test_job_cancel(self):
        params = dict(
            start_date='2018-05-10 21:51',  # we have an event here
            end_date='2018-05-10 21:52',
        )
        job = self.ds.request_datafile(
            **params
        )
        status = job.get_status()

        try:
            job.cancel()
        except APIException as exception:
            # cancel raised an exception, means that we were already processing it
            if status == 'processing':
                assert exception.response.status_code == 400
            else:
                assert status == 'enqueued'
                assert job.get_status() == 'cancelled'

                assert job.is_processing is False
                with pytest.raises(JobNotProcessing):
                    job.wait_for_completion()

    @classmethod
    def teardown_class(cls):
        cls.ds.delete()
