import logging

import requests

from ravenpackapi.exceptions import api_method
from ravenpackapi.utils.constants import JSON_AVAILABLE_FIELDS
from .job import Job
from .results import Results, Result

logger = logging.getLogger('ravenpack.models.dataset')


class Dataset(object):
    _READ_ONLY_FIELDS = {'creation_time', 'last_modified', 'uuid'}
    _VALID_FIELDS = {'name', 'description',
                     'tags', 'product', 'product_version',
                     'frequency', 'fields', 'filters', } | _READ_ONLY_FIELDS

    def __init__(self, api=None, **kwargs):
        """
        :type api: RPApi
        """
        super(Dataset, self).__init__()
        self._data = kwargs
        self.api = api
        # the dataset can be initialized with just the uuid
        # in that case we'll ask the server for the missing info
        additional_fields = {k for k in kwargs if k != 'uuid'}
        self.complete_from_server = len(additional_fields) >= 1

    @staticmethod
    def from_dict(item, api=None):
        return Dataset(
            api=api,
            **{k: v for k, v in item.items() if k in Dataset._VALID_FIELDS}
        )

    def __setattr__(self, field, value):
        if field in Dataset._READ_ONLY_FIELDS:
            raise ValueError("The field %s is ReadOnly" % field)
        if field == 'id':
            field = 'uuid'
        if field in Dataset._VALID_FIELDS:
            self._data[field] = value
        else:
            return super(Dataset, self).__setattr__(field, value)

    @property
    def id(self):  # an alias for the dataset unique id
        return self.uuid

    def __getattr__(self, field):
        if field in Dataset._VALID_FIELDS:
            if field not in self._data:
                self.get_from_server()
            return self._data[field]
        else:
            return self.__getattribute__(field)

    def as_dict(self):
        valid_obj = {k: self._data[k]
                     for k in Dataset._VALID_FIELDS
                     if k in self._data}
        return valid_obj

    def __str__(self):
        return "Dataset: {name} [{id}]".format(
            name=self.name, id=self.id,
        )

    @api_method
    def get_from_server(self, force=False):
        """ Get the dataset definition from the server,
            if needed or forced """
        dataset_id = self.id
        if not dataset_id:
            raise ValueError("Please specify a dataset ID to retrieve it from server")
        if not self.complete_from_server or force:
            logger.debug("Getting Dataset from server %s" % dataset_id)
            response = self.api.request(
                endpoint="/datasets/{dataset_uuid}".format(dataset_uuid=dataset_id),
            )
            self._data = response.json()
            self.complete_from_server = True
        return self._data

    @api_method
    def delete(self):
        """ Delete the dataset """
        self.api.request(
            endpoint="/datasets/{dataset_uuid}".format(dataset_uuid=self.id),
            method='delete',
        )

    @api_method
    def save(self):
        response = self.api.request(
            endpoint="/datasets",
            data=self.as_dict(),
            method='post'
        )

        dataset_id = response.json()['dataset_uuid']
        logger.info("Created dataset %s" % dataset_id)
        self._data['uuid'] = dataset_id

    @api_method
    def json(self,
             start_date,
             end_date,
             fields=None,
             time_zone=None,
             frequency='granular',
             having=None,
             ):
        """ Use the dataset filters to request a data

        Some limitation applies:
        * granular datasets: 10,000 records
        * indicator datasets: 500 entities, timerange 1Y, lookback 1Y
        """
        api = self.api
        dataset_id = self.id
        if fields is None:
            # fields are required, if it's not provided we use
            # the dataset ones
            fields = self.fields

        # let's build the body, with all the defined fields
        body = {}
        for k in JSON_AVAILABLE_FIELDS:
            if locals().get(k) is not None:
                body[k] = locals().get(k)

        response = api.request(
            endpoint="/json/{dataset_uuid}".format(dataset_uuid=dataset_id),
            method='post',
            data=body,
        )
        data = response.json()
        return Results(data['records'],
                       name='JSON query for %s' % dataset_id)

    @api_method
    def request_datafile(self, start_date, end_date,
                         output_format='csv',
                         compressed=False,
                         tags=None,
                         notify=False):
        api = self.api
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "format": output_format,
            "compressed": compressed,
            "notify": notify,
        }
        if tags:
            data['tags'] = tags
        response = api.request(
            endpoint="/datafile/%s" % self.id,
            data=data,
            method='post',
        )
        job = Job(api=self.api,
                  token=response.json()['token'])  # an undefined job, has just the token
        return job

    @api_method
    def request_realtime(self):
        api = self.api
        endpoint = "{base}/{dataset_id}".format(base=api._FEED_BASE_URL,
                                                dataset_id=self.id)
        logger.debug("Connecting with RT feed: %s" % endpoint)
        r = requests.get(endpoint,
                         headers=api.headers,
                         stream=True,
                         )

        for line in r.iter_lines():
            yield Result(line)
