import json
import logging
import os
from time import sleep

import requests

from ravenpackapi import Dataset
from ravenpackapi.exceptions import APIException
from ravenpackapi.models.dataset import DatasetList
from ravenpackapi.models.job import Job
from ravenpackapi.util import to_curl

_VALID_METHODS = ('get', 'post', 'put', 'delete')

logger = logging.getLogger("ravenpack.core")


class RPApi(object):
    _BASE_URL = os.environ.get('RP_API_ENDPOINT', 'https://api.ravenpack.com/1.0')
    _FILE_AVAILABILIY_SECONDS_DELAY = 5.0
    _CHUNK_SIZE = 1024 * 32

    def __init__(self, api_key):
        api_key = api_key or os.environ.get('RP_API_KEY')
        if api_key is None:
            raise ValueError(
                "Please initialize with an api_key "
                "or set your environment RP_API_KEY with a permanent token"
            )
        self.api_key = api_key

    def request(self, endpoint, data=None, method='get'):
        assert method in _VALID_METHODS, 'Method {used} not accepted. Please use {valid_methods}'
        logger.debug("Request to %s" % endpoint)
        requests_call = getattr(requests, method)
        logger.debug("Request {method} to {endpoint}".format(method=method,
                                                             endpoint=endpoint))
        response = requests_call(
            url=self._BASE_URL + endpoint,
            headers=dict(API_KEY=self.api_key),
            data=json.dumps(data) if data else None,
        )
        if response.status_code != 200:
            logger.error("Error calling the API, we tried: %s" % to_curl(response.request))
            raise APIException('Got an error {status}: {error_message}'.format(
                status=response.status_code, error_message=response.text
            ), response=response)
        return response

    def list_datasets(self, tags=None, scope=None):
        """ Return a DataSetList of datasets in the scope """
        response = self.request('/datasets', data=dict(
            tags=tags or [],
            scope=scope or 'private',
        ))
        return DatasetList(map(Dataset.from_dict, response.json()['datasets']))

    def create_dataset(self, dataset):
        response = self.request(endpoint="/datasets",
                                data=dataset.as_dict(),
                                method='post')
        dataset_id = response.json()['dataset_uuid']
        logger.info("Created dataset %s" % dataset_id)
        return dataset_id

    def download_dataset(self, dataset_id, start_date, end_date,
                         output_format='csv', compressed=False, notify=False):
        response = self.request(
            endpoint="/datafile/%s" % dataset_id,
            data={
                "start_date": start_date,
                "end_date": end_date,
                "format": output_format,
                "compressed": compressed,
                "notify": notify,
            },
            method='post',
        )
        job = Job(response.json()['token'])  # an undefined job, has just the token
        return job

    def get_job_status(self, job):
        token = job.token
        response = self.request(
            endpoint="/jobs/%s" % token,
            data={
                "token": token,
            },
            method='get',
        )
        return Job(token, **response.json())

    def wait_job_to_be_ready(self, job):
        logger.info("Waiting for the job to be ready...")
        while True:
            try:
                job = self.get_job_status(job)
            except APIException:  # keep waiting if API raises exceptions
                sleep(self._FILE_AVAILABILIY_SECONDS_DELAY)
                continue
            if not job.is_processing:
                return job
            sleep(self._FILE_AVAILABILIY_SECONDS_DELAY)

    def save_job_to_file(self, job, filename):
        with open(filename, 'wb') as output:
            job = self.wait_job_to_be_ready(job)
            logger.info(u"Writing to %s" % filename)

            r = requests.get(job.url,
                             headers=dict(API_KEY=self.api_key),
                             stream=True,
                             )

            for chunk in r.iter_content(chunk_size=self._CHUNK_SIZE):
                if chunk:
                    output.write(chunk)
