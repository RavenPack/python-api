from ravenpackapi.util import to_curl


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class TestToCurl(object):
    def test_normal_curl(self):
        request = AttrDict(
            method="GET", headers={"API-KEY": "test"}, body=None, url="http://test"
        )
        assert to_curl(request) == "curl -X GET -H 'API-KEY:test' 'http://test'"

    def test_missing_request(self):
        assert to_curl(None) == "No request"
