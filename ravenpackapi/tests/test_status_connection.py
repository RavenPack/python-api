import pytest
from urllib3.exceptions import InsecureRequestWarning

from ravenpackapi import RPApi


class TestEntityMapping(object):
    def test_status(self):
        api = RPApi()
        status = api.get_status()
        assert status.get('status') == 'OK'

    def test_status_no_https_verify(self):
        api = RPApi()
        api.common_request_params['verify'] = False
        with pytest.warns(InsecureRequestWarning):
            status = api.get_status()
            assert status.get('status') == 'OK'
