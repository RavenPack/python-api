import pytest

from ravenpackapi.exceptions import APIException, APIException425
from ravenpackapi.upload.upload_utils import retry_on_too_early


class TestRetryOnTooEarly:
    def test_fails_if_not_enough_retries(self):
        eventually_success = EventuallySuccess(num_calls_to_fail=10)
        with pytest.raises(APIException425):
            retry_on_too_early(eventually_success, 1, 2, 3, namearg="namevalue")
        assert eventually_success.num_calls == 10
        assert eventually_success.calls == [((1, 2, 3), {"namearg": "namevalue"})] * 10
        3
        min_wait, max_wait = 3 * 2 ** 9, 3 * 2 ** 10
        assert min_wait < self.seconds_slept <= max_wait

    def test_succeeds_eventually(self):
        eventually_success = EventuallySuccess(num_calls_to_fail=9)
        retry_on_too_early(eventually_success, 1, 2, 3, namearg="namevalue")
        assert eventually_success.num_calls == 10
        assert eventually_success.calls == [((1, 2, 3), {"namearg": "namevalue"})] * 10

    def test_only_handles_api_exception_425(self):
        eventually_success = EventuallySuccess(
            num_calls_to_fail=100, error_to_raise=APIException
        )
        with pytest.raises(APIException):
            retry_on_too_early(eventually_success, 1, 2, 3, namearg="namevalue")
        assert eventually_success.num_calls == 1
        assert eventually_success.calls == [((1, 2, 3), {"namearg": "namevalue"})]
        assert self.seconds_slept == 0

    @pytest.fixture(autouse=True)
    def mocked_sleep(self, mocker):
        self.seconds_slept = 0

        def sleep(seconds):
            self.seconds_slept += seconds

        time = mocker.patch("tenacity.nap.time")
        time.sleep.side_effect = sleep
        return time.sleep


class EventuallySuccess:
    def __init__(self, num_calls_to_fail=0, error_to_raise=APIException425):
        self.num_calls_to_fail = num_calls_to_fail
        self.num_calls = 0
        self.error_to_raise = error_to_raise
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        self.num_calls += 1
        if self.num_calls <= self.num_calls_to_fail:
            raise self.error_to_raise
        return self.num_calls
