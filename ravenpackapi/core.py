import logging
import os

from ravenpackapi import Dataset
from ravenpackapi.exceptions import get_exception
from ravenpackapi.key_events.module import KeyEventsApi
from ravenpackapi.models.dataset_list import DatasetList
from ravenpackapi.models.job import Job
from ravenpackapi.models.mapping import RPMappingResults
from ravenpackapi.models.reference import RpEntityReference, EntityTypeReference
from ravenpackapi.models.results import Results
from ravenpackapi.upload.module import UploadApi
from ravenpackapi.util import to_curl
from ravenpackapi.utils.date_formats import as_datetime_str, as_date_str
from ravenpackapi.utils.dynamic_sessions import DynamicSession

_VALID_METHODS = ('get', 'post', 'put', 'delete', 'patch')
VERSION = '1.0.55'

logger = logging.getLogger("ravenpack.core")

DEFAULT_ENDPOINTS = {
    "api": {
        "rpa": 'https://api.ravenpack.com/1.0',
        "edge": 'https://api-edge.ravenpack.com/1.0',
    },
    "feed": {
        "rpa": 'https://feed.ravenpack.com/1.0/json',
        "edge": 'https://feed-edge.ravenpack.com/1.0/json',
    }
}


class RPApi(object):
    _CHUNK_SIZE = 32 * 1024
    common_request_params = {
        "timeout": (10, 60),  # 10 seconds on connection - 60 on read
    }

    def __init__(self, api_key=None, product="rpa"):
        if product not in DEFAULT_ENDPOINTS['api']:
            raise ValueError("Unknown product %s "
                             "- please specify either 'rpa' or 'edge'" % product)
        self._BASE_URL = os.environ.get(
            'RP_API_ENDPOINT',
            DEFAULT_ENDPOINTS["api"][product],
        )
        self._FEED_BASE_URL = os.environ.get(
            'RP_FEED_ENDPOINT',
            DEFAULT_ENDPOINTS["feed"][product]
        )
        self._UPLOAD_BASE_URL = os.environ.get(
            'RP_UPLOAD_ENDPOINT',
            'https://upload.ravenpack.com/1.0')
        api_key = api_key or os.environ.get('RP_API_KEY')
        if api_key is None:
            raise ValueError(
                "Please initialize with an api_key "
                "or set your environment RP_API_KEY with your API KEY."
            )
        self.api_key = api_key
        self.log_curl_commands = True
        self.session = DynamicSession()
        self.upload = UploadApi(self)
        self.insider_trasactions = KeyEventsApi(self, "insider-transactions")
        self.earnings_dates = KeyEventsApi(self, "earnings-dates")
        self.product = product

    @property
    def headers(self):
        return {"API_KEY": self.api_key,
                'User-Agent': 'RavenPack Python v%s' % VERSION,
                }

    def request(self, endpoint, data=None, json=None,
                params=None, method='get', stream=False,
                request_params=None,
                headers=None,
                except_on_fail=True):
        assert method in _VALID_METHODS, \
            'Method {used} not accepted. Please choose one of {valid_methods}'.format(
                used=method, valid_methods=", ".join(_VALID_METHODS)
            )
        requests_call = getattr(self.session, method)
        logger.debug("Request {method} to {endpoint}".format(method=method,
                                                             endpoint=endpoint))
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            # calling another host
            url = endpoint
        else:
            url = self._BASE_URL + endpoint

        extra_params = self.common_request_params.copy()
        if request_params:
            extra_params.update(request_params)
        response = requests_call(
            url=url,
            headers=self.headers if headers is None else headers,
            data=data,
            json=json,
            params=params,
            stream=stream,
            **extra_params
        )
        if self.log_curl_commands:
            logger.info("API query to %s" % to_curl(response.request))
        if except_on_fail and response.status_code not in {200, 202}:
            logger.error("Error calling the API, we tried: %s" % to_curl(response.request))
            raise get_exception(response)
        return response

    def list_datasets(self, scope=None, tags=None, product=None):
        """ Return a DataSetList of datasets in the scope """
        response = self.request('/datasets', params=dict(
            tags=tags or None,
            scope=scope or 'private',
            product=product or self.product,
        ))
        return DatasetList(
            map(lambda item: Dataset.from_dict(item, api=self),
                response.json()['datasets'])
        )

    def list_jobs(self, start_date, end_date, status=None):
        response = self.request('/jobs', params={
            "start_date": as_datetime_str(start_date),
            "end_date": as_datetime_str(end_date),
            "status": status
        })
        return [Job(self, job) for job in response.json()['jobs']]

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
             fields=None,
             filters=None,
             time_zone=None,
             frequency='granular',
             having=None,
             custom_fields=None,
             conditions=None,
             product=None,
             product_version='1.0',
             ):
        # let's build the body, with all the defined fields
        if product is None:
            product = self.product
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
            product=product,
            product_version=product_version,
        ))

        response = self.request(
            endpoint="/json",
            method='post',
            json={k: v for k, v in body.items() if v is not None},  # remove null values
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

    def get_entity_type_reference(self,
                                  entity_type=None,
                                  reference_type='full',
                                  date=None):
        if entity_type:
            entity_type = entity_type.upper()
        params = {"entity_type": entity_type,
                  "type": reference_type,
                  "date": as_date_str(date) if date else None}
        response = self.request(
            endpoint="/entity-reference",
            method='get',
            params={k: v for k, v in params.items() if v},  # exclude missing params
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
            json={
                "identifiers": identifiers
            },
        )
        data = response.json()
        return RPMappingResults(data)

    def get_status(self):
        response = self.request('/status')
        return response.json()

    def get_document_url(self, rp_story_id):
        response = self.request('/document/%s/url' % rp_story_id)
        return response.json()['url']

    def get_flatfile_list(self, flatfile_type):
        assert flatfile_type in {
            'companies', 'full'
        }
        response = self.request('/history/%s' % flatfile_type)
        return response.json()

    def get_flatfile(self, flatfile_type, flatfile_id):
        """ Request the flatfile and return a streammable response """
        return self.request(
            '/history/%(flatfile_type)s/%(flatfile_id)s' % dict(
                flatfile_type=flatfile_type,
                flatfile_id=flatfile_id,
            ),
            stream=True,
        )

    def save_flatfile(self, flatfile_type, flatfile_id, output_filename, overwrite=True):
        if not overwrite and os.path.isfile(output_filename):
            return False  # the file already exists

        with self.get_flatfile(flatfile_type, flatfile_id) as flatzip:
            with open(output_filename, 'wb') as f:
                for chunk in flatzip.iter_content(chunk_size=8192):
                    f.write(chunk)
