import logging

import pytest

from ravenpackapi.core import RPApi
from ravenpackapi.exceptions import APIException
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

    def test_api_key_not_logged(self, api, dynamic_session, caplog):
        response = dynamic_session.get.return_value
        response.status_code = 403
        response.request.method = "GET"
        response.request.url = "https://api-edge.ravenpack.com/1.0/datasets"
        response.request.headers = api.headers
        response.request.body = None

        with caplog.at_level(logging.INFO):
            with pytest.raises(APIException):
                api.request("/datasets")
        assert "Error calling the API" in caplog.text
        assert api.api_key not in caplog.text

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
