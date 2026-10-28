import pytest

from ravenpackapi.util import get_python_version, to_curl


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class TestToCurl(object):
    def test_normal_curl(self):
        request = AttrDict(
            method="GET", headers={"X-Custom": "test"}, body=None, url="http://test"
        )
        assert to_curl(request) == "curl -X GET -H 'X-Custom:test' 'http://test'"

    @pytest.mark.parametrize("header", ["API_KEY", "API-KEY", "Authorization"])
    def test_credentials_are_redacted(self, header):
        request = AttrDict(
            method="GET", headers={header: "s3cr3t"}, body=None, url="http://test"
        )
        curl = to_curl(request)
        assert "s3cr3t" not in curl
        assert curl == "curl -X GET -H '%s:<REDACTED>' 'http://test'" % header

    def test_missing_request(self):
        assert to_curl(None) == "No request"


def test_get_python_version():
    python_version = get_python_version()
    pyver_int = int(python_version.replace(".", ""))
    assert pyver_int == 27 or 31 <= pyver_int <= 39 or 310 <= pyver_int <= 399
