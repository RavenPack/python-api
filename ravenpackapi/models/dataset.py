import logging

import requests
import urllib3

from ravenpackapi.exceptions import api_method, APIException, ApiConnectionError
from ravenpackapi.util import to_curl
from ravenpackapi.utils.date_formats import as_datetime_str
from .job import Job
from .results import Results, Result

logger = logging.getLogger('ravenpack.models.dataset')


class Dataset(object):
    _READ_ONLY_FIELDS = {'creation_time', 'last_modified', 'uuid'}
    _VALID_FIELDS = {'name', 'description',
                     'tags', 'product', 'product_version',
                     'frequency', 'fields', 'filters', 'tags',
                     'having', 'custom_fields', 'conditions',
                     } | _READ_ONLY_FIELDS
    _NULLABLE_FIELDS = {'fields'}

    def __init__(self, api=None, name=None,
                 description=None, tags=None,
                 product="RPA", product_version="1.0",
                 frequency=None, fields=None, filters=None,
                 custom_fields=None, conditions=None,
                 having=None,
                 uuid=None,  # id is just an alias of uuid
                 **kwargs
                 ):
        """
        :type api: RPApi
        """
        super(Dataset, self).__init__()

        if 'id' in kwargs:
            if uuid:
                raise Exception("Please provide or the id or the uuid, not both: they are aliases")
            uuid = kwargs.pop('id')

        self.api = api
        self.product_version = product_version
        self.product = product

        self.uuid = uuid

        self.name = name
        self.description = description

        self.fields = fields
        self.filters = filters
        self.frequency = frequency
        self.custom_fields = custom_fields
        self.conditions = conditions
        self.having = having

        self.tags = tags

        self.creation_time = kwargs.pop('creation_time', None)
        self.last_modified = kwargs.pop('last_modified', None)

        if kwargs:
            raise ValueError("Invalid fields for the dataset: %s" % ", ".join(kwargs.keys()))

        # the dataset can be initialized with just the uuid and the name
        # in that case we'll ask the server for the missing info
        self._lazy_retrieve_on_get = True

    @staticmethod
    def from_dict(item, api=None):
        return Dataset(
            api=api,
            **{k: v for k, v in item.items() if k in Dataset._VALID_FIELDS}
        )

    def __setattr__(self, field, value):
        if field == 'id':
            field = 'uuid'
        if field in Dataset._VALID_FIELDS:
            self._lazyload()
            super(Dataset, self).__setattr__(field, value)
        else:
            object.__setattr__(self, field, value)

    def __delitem__(self, field):
        if field == 'id':
            field = 'uuid'
        setattr(self, field, None)

    @property
    def id(self):  # an alias for the dataset unique id
        return self.uuid

    def _lazyload(self):
        if (getattr(self, '_lazy_retrieve_on_get', False)  # dynamic, we check this also during object creation
            and self.uuid
        ):
            self.get_from_server()  # get the missing fields

    def __getattribute__(self, field):
        """ Getting attributes we may trigger a data refresh from the server """
        if field == 'id':  # id is an alias for uuid
            field = 'uuid'

        # print('asking for', field)
        # value = super(Dataset, self).__getattribute__(field)
        # return value

        if field in Dataset._VALID_FIELDS and field != 'uuid':
            value = super(Dataset, self).__getattribute__(field)
            if value is None:
                self._lazyload()
        return super(Dataset, self).__getattribute__(field)

    def as_dict(self):
        valid_obj = {
            k: getattr(self, k)
            for k in Dataset._VALID_FIELDS
        }
        return valid_obj

    def __str__(self):
        return "Dataset: {name} [{id}]".format(
            name=self.name, id=self.id,
        )

    @api_method
    def get_from_server(self, force=False):
        """ Get the dataset definition from the server,
            if needed or forced """
        dataset_id = self.uuid
        if not dataset_id:
            raise ValueError("Please specify a dataset ID to retrieve it from server")
        if self._lazy_retrieve_on_get or force:
            logger.debug("Getting Dataset from server %s" % dataset_id)
            response = self.api.request(
                endpoint="/datasets/{dataset_uuid}".format(dataset_uuid=dataset_id),
            )
            self._lazy_retrieve_on_get = False  # we got everything from the server
            for field, value in response.json().items():
                setattr(self, field, value)
        return self.as_dict()

    @api_method
    def delete(self):
        """ Delete the dataset """
        self.api.request(
            endpoint="/datasets/{dataset_uuid}".format(dataset_uuid=self.id),
            method='delete',
        )

    @api_method
    def save(self):
        if self.id is None:
            # creating a new dataset
            verb = 'Created'
            method = 'post'
            if not self.product_version:
                # we explicitly create as version 1.0
                self.product_version = '1.0'
            endpoint = "/datasets"
        else:
            verb = 'Updated'
            endpoint = "/datasets/%s" % self.id
            method = 'put'

        # get rid of the readonly fields
        data = {
            k: v for k, v in self.as_dict().items()
            if (k not in Dataset._READ_ONLY_FIELDS
                and v is not None
                )
        }

        if 'frequency' in data and 'fields' not in data:
            # fields can be null, we specify it only when frequency is also given
            data['fields'] = self.fields

        response = self.api.request(
            endpoint=endpoint,
            json=data,
            method=method
        )
        dataset_id = response.json()['dataset_uuid']
        logger.info("{verb} dataset {id}".format(
            verb=verb,
            id=dataset_id)
        )
        self._lazy_retrieve_on_get = False
        self.uuid = dataset_id

    @api_method
    def json(self,
             start_date,
             end_date,
             fields=None,
             time_zone=None,
             frequency=None,
             having=None,
             custom_fields=None,
             filters=None,
             conditions=None,
             ):
        """ Use the dataset filters to request a data

        Some limitation applies:
        * granular datasets: 10,000 records
        * indicator datasets: 500 entities, timerange 1Y, lookback 1Y
        """
        api = self.api
        dataset_id = self.id

        # let's build the body, with all the defined fields
        body = {"start_date": as_datetime_str(start_date),
                "end_date": as_datetime_str(end_date),
                "time_zone": time_zone}
        body.update(dict(
            frequency=frequency,
            fields=fields,
            custom_fields=custom_fields,
            filters=filters,
            conditions=conditions,
            having=having,
        ))

        response = api.request(
            endpoint="/json/{dataset_uuid}".format(dataset_uuid=dataset_id),
            method='post',
            json={k: v for k, v in body.items() if v is not None},  # remove null values
        )
        data = response.json()
        return Results(data['records'],
                       name='JSON query for %s' % dataset_id)

    @api_method
    def count(self, start_date, end_date, time_zone=None):
        """ Get the count of stories, analytics records and entities over a period
        """
        api = self.api
        dataset_id = self.id

        # let's build the body, with all the defined fields
        body = {"start_date": as_datetime_str(start_date),
                "end_date": as_datetime_str(end_date),
                "time_zone": time_zone}

        response = api.request(
            endpoint="/datafile/{dataset_uuid}/count".format(dataset_uuid=dataset_id),
            method='post',
            json={k: v for k, v in body.items() if v is not None}
        )
        return response.json()

    @api_method
    def request_datafile(self, start_date, end_date,
                         output_format='csv',
                         compressed=False,
                         tags=None,
                         notify=False,
                         allow_empty=True,
                         time_zone='UTC',
                         fields=None,
                         ):
        """ Request a datafile with data in the requested date
            This is asyncronous: it returns a job that you can wait for
            if allow_empty is True, it may return None meaning that the job will have no data
        """
        api = self.api
        data = {
            "start_date": as_datetime_str(start_date),
            "end_date": as_datetime_str(end_date),
            "format": output_format,
            "compressed": compressed,
            "notify": notify,
            "time_zone": time_zone,
            "tags": tags,
            "fields": fields,
        }
        try:
            response = api.request(
                endpoint="/datafile/%s" % self.id,
                json={k: v for k, v in data.items() if v is not None},  # remove null values,
                method='post',
            )
        except APIException as e:
            if e.response.status_code == 400 and allow_empty:
                errors = [e['type'] for e in e.response.json()['errors']]
                if 'DatafileEmptyError' in errors:
                    return None
            raise e
        job = Job(api=self.api,
                  token=response.json()['token'])  # an undefined job, has just the token
        return job

    @api_method
    def request_realtime(self):
        api = self.api
        endpoint = "{base}/{dataset_id}?keep_alive".format(base=api._FEED_BASE_URL,
                                                           dataset_id=self.id)
        logger.debug("Connecting with RT feed: %s" % endpoint)
        try:
            response = api.session.get(endpoint,
                                       headers=api.headers,
                                       stream=True,
                                       **api.common_request_params
                                       )
            if response.status_code != 200:
                logger.error("Error calling the API, we tried: %s" % to_curl(response.request))
                raise APIException(
                    'Got an error {status}: body was \'{error_message}\''.format(
                        status=response.status_code,
                        error_message=response.text
                    ), response=response)
            response.encoding = 'utf-8'

            for line in response.iter_lines(decode_unicode=True, chunk_size=1):
                if line:  # skip empty lines to support keep-alive
                    yield Result(line)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError,
                urllib3.exceptions.ProtocolError,
                requests.exceptions.Timeout):
            raise ApiConnectionError()
