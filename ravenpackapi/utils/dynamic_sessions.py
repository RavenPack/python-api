from collections import defaultdict
from functools import partial

import requests
from six.moves.urllib.parse import urlparse

_REQUESTS_METHODS = ('get', 'post', 'put', 'delete', 'patch')


# see test_dynamic_sessions.py for how to use it

class DynamicSession(object):
    """ This looks intricate but its a way to make requests.session work transparently creating different
        session depending on the hostname of the urls
    """
    _session_by_host = defaultdict(requests.session)

    @staticmethod
    def get_session_from_args(args, kwargs):
        url = kwargs.get('url', None)
        if url is None:
            url = args[0]  # get the positional url
        parsed_uri = urlparse(url)
        session_key = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        if 'verify' in kwargs:
            session_key += "-noverify"  # unverified calls get a different session
        session = DynamicSession._session_by_host[session_key]
        return session

    @staticmethod
    def get_session_method(method, *args, **kwargs):
        # this will be returned as a partial - it will get a session for the url in the call
        # that will get the proper session for that host
        session = DynamicSession.get_session_from_args(args, kwargs)
        return getattr(session, method)(*args, **kwargs)

    @staticmethod
    def __getattr__(method):
        # when we do DynamicSession.post - it will return a partial - that will ask to get
        if method in _REQUESTS_METHODS:
            return partial(DynamicSession.get_session_method, method)
        return getattr(requests, method)

    @staticmethod
    def get_session(*args, **kwargs):
        """ This is the only method that is only from here - everything else is taken from requests """
        return DynamicSession.get_session_from_args(args, kwargs)
