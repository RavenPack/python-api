from functools import wraps

import requests


class APIException(Exception):
    def __init__(self, *args, **kwargs):
        response = kwargs.pop('response', None)
        super(APIException, self).__init__(*args)
        self.response = response


class MissingAPIException(Exception):
    def __str__(self):
        return "Define the api parameter with your own APIKEY " \
               "to access the API methods from a model"


class DataFileTimeout(Exception):
    pass


class JobNotProcessing(Exception):
    def __init__(self, *args, **kwargs):
        status = kwargs.pop('status', None)
        super(JobNotProcessing, self).__init__(*args)
        self.status = status


def api_method(func):
    @wraps(func)
    def decorated_func(instance, *args, **kwargs):
        if not getattr(instance, 'api'):
            raise MissingAPIException()
        return func(instance, *args, **kwargs)

    return decorated_func


class ValidationError(Exception):
    pass


class ApiConnectionError(requests.ConnectionError):
    pass
