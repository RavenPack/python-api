from functools import wraps

import requests


def get_exception(response):
    """ Return an appropriate APIException given an API response """
    if response.status_code == 404:
        Exception_class = APIException404
    elif response.status_code == 425:
        Exception_class = APIException425
    else:
        Exception_class = APIException

    return Exception_class(
        'Got an error {status}: body was \'{error_message}\''.format(
            status=response.status_code,
            error_message=response.text
        ), response=response)


class APIException(Exception):
    def __init__(self, *args, **kwargs):
        response = kwargs.pop('response', None)
        super(APIException, self).__init__(*args)
        self.response = response


class APIException404(APIException):
    pass


class APIException425(APIException):
    """ Request arrived too early """
    pass


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
