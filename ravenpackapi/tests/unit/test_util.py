from ravenpackapi.util import get_python_version, to_curl


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


def test_get_python_version():
    python_version = get_python_version()
    pyver_int = int(python_version.replace(".", ""))
    assert pyver_int == 27 or 31 <= pyver_int <= 39 or 310 <= pyver_int <= 399
