import json
import logging
import os

import requests

from ravenpackapi import Dataset
from ravenpackapi.exceptions import APIException
from ravenpackapi.models.dataset_list import DatasetList
from ravenpackapi.models.mapping import RPMappingResults
from ravenpackapi.models.reference import RpEntityReference, EntityTypeReference
from ravenpackapi.models.results import Results
from ravenpackapi.util import to_curl
from ravenpackapi.utils.constants import JSON_AVAILABLE_FIELDS, ENTITY_TYPES

_VALID_METHODS = ('get', 'post', 'put', 'delete')
VERSION = '1.0.23'

logger = logging.getLogger("ravenpack.core")


class RPApi(object):
    _CHUNK_SIZE = 32 * 1024

    def __init__(self, api_key=None):
        self._BASE_URL = os.environ.get(
            'RP_API_ENDPOINT',
            'https://api.ravenpack.com/1.0')
        self._FEED_BASE_URL = os.environ.get(
            'RP_FEED_ENDPOINT',
            'https://feed.ravenpack.com/1.0/json'
        )
        api_key = api_key or os.environ.get('RP_API_KEY')
        if api_key is None:
            raise ValueError(
                "Please initialize with an api_key "
                "or set your environment RP_API_KEY with your API KEY."
            )
        self.api_key = api_key
        self.log_curl_commands = True

    @property
    def headers(self):
        return {"API_KEY": self.api_key,
                'User-Agent': 'RavenPack Python v%s' % VERSION,
                }

    def request(self, endpoint, data=None, params=None, method='get', stream=False):
        assert method in _VALID_METHODS, \
            'Method {used} not accepted. Please choose one of {valid_methods}'.format(
                used=method, valid_methods=", ".join(_VALID_METHODS)
            )
        requests_call = getattr(requests, method)
        logger.debug("Request {method} to {endpoint}".format(method=method,
                                                             endpoint=endpoint))
        response = requests_call(
            url=self._BASE_URL + endpoint,
            headers=self.headers,
            data=json.dumps(data) if data else None,
            params=params,
            stream=stream,
        )
        if self.log_curl_commands:
            logger.info("API query to %s" % to_curl(response.request))
        if response.status_code != 200:
            logger.error("Error calling the API, we tried: %s" % to_curl(response.request))
            raise APIException(
                'Got an error {status}: body was \'{error_message}\''.format(
                    status=response.status_code,
                    error_message=response.text
                ), response=response)
        return response

    def list_datasets(self, scope=None, tags=None, options=None):
        """ Return a DataSetList of datasets in the scope """
        response = self.request('/datasets', params=dict(
            tags=tags or None,
            scope=scope or 'private',
        ))
        datasets = DatasetList(
            map(lambda item: Dataset.from_dict(item, api=self),
                response.json()['datasets'])
        )

        # Wasn't clear that when calling this function a class object was returned
        # looking to return just a list of the datasets and its associated info.
        # This change doesn't need to happen, but I had to dig through the source code
        if options == 'by_name':
            return datasets.by_name
        if options == 'by_id':
            return datasets.by_id
        else:
            return datasets

    def create_dataset(self, dataset):
        # be sure to create a copy
        new_dataset_data = dataset.as_dict()
        new_dataset = Dataset(api=self,
                              **new_dataset_data)
        if 'uuid' in new_dataset_data:
            del new_dataset['uuid']
        new_dataset.save()
        dataset_id = new_dataset.id
        logger.info("Created dataset %s" % dataset_id)
        return new_dataset

    def get_dataset(self, dataset_id):
        return Dataset(
            api=self,
            uuid=dataset_id,
        )

    def json(self,
             start_date,
             end_date,
             fields,
             filters=None,
             time_zone=None,
             frequency='granular',
             having=None,
             product='rpa',
             product_version='1.0',
             ):
        # let's build the body, with all the defined fields
        body = {}
        for k in JSON_AVAILABLE_FIELDS:
            if locals().get(k) is not None:
                body[k] = locals().get(k)

        response = self.request(
            endpoint="/json",
            method='post',
            data=body,
        )
        data = response.json()
        return Results(data['records'],
                       name='Ad-hoc JSON query')

    def get_entity_reference(self, rp_entity_id):
        response = self.request(
            endpoint="/entity-reference/%s" % rp_entity_id,
        )
        data = response.json()
        return RpEntityReference(rp_entity_id, data)

    def get_entity_type_reference(self, entity_type=None):
        if entity_type:
            entity_type = entity_type.upper()
        assert entity_type in ENTITY_TYPES, "Please provide a valid entity type, one of %s" % ENTITY_TYPES
        response = self.request(
            endpoint="/entity-reference",
            method='get',
            params={"entity_type": entity_type} if entity_type else None,
            stream=True,
        )
        return EntityTypeReference(http_response=response)

    @staticmethod
    def get_entity_type_reference_from_file(file_path):
        return EntityTypeReference(file_path=file_path)

    def get_entity_mapping(self, identifiers):
        response = self.request(
            endpoint="/entity-mapping",
            method='post',
            data={
                "identifiers": identifiers
            },
        )
        data = response.json()
        return RPMappingResults(data)


