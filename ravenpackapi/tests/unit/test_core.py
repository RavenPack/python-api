import pytest

from ravenpackapi.core import RPApi
from ravenpackapi.util import get_python_version
from ravenpackapi.version import __version__


class TestRPApiRequests:
    def test_request_get(self, api, dynamic_session):
        assert len(__version__.split(".")) >= 3
        python_version = get_python_version()
        response = api.request("/datasets")
        user_agent = "RavenPack Python " + python_version + " " + "v" + __version__
        dynamic_session.get.assert_called_with(
            url="https://api-edge.ravenpack.com/1.0/datasets",
            headers={"API_KEY": api.api_key, "User-Agent": user_agent},
            timeout=(10, 100),
            data=None,
            params=None,
            stream=False,
            json=None,
        )
        assert response.status_code == 200

    @pytest.fixture
    def api(self, dynamic_session):
        api = RPApi(api_key="123abc", product="edge")
        api.session = dynamic_session
        return api

    @pytest.fixture
    def dynamic_session(self, mocker):
        session = mocker.patch("ravenpackapi.core.DynamicSession")
        session.get.return_value.status_code = 200
        return session
