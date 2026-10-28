import pytest

from ravenpackapi.exceptions import APIException, DataFileTimeout
from ravenpackapi.models.job import Job


class FailingAPI(object):
    """An API whose job status endpoint always fails"""

    def __init__(self):
        self.calls = 0

    def request(self, *args, **kwargs):
        self.calls += 1
        raise APIException("Got an error 503")


class TestJobWaitForCompletion:
    def test_timeout_fires_while_api_keeps_failing(self):
        api = FailingAPI()
        job = Job(api, token="TOKEN", status="processing")
        job._FILE_AVAILABILIY_SECONDS_DELAY = 0.01

        with pytest.raises(DataFileTimeout):
            job.wait_for_completion(timeout_seconds=0.1)
        assert api.calls < 10
