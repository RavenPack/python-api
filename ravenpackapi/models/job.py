import datetime
import logging
from time import sleep

import requests

from ravenpackapi.exceptions import api_method, APIException, DataFileTimeout

logger = logging.getLogger(__name__)


class Job(object):
    _VALID_FIELDS = {'token', 'status', 'size',
                     'url', 'checksum'}
    _FILE_AVAILABILIY_SECONDS_DELAY = 5.0
    _CHUNK_SIZE = 1024 * 32

    def __init__(self, api, token, **kwargs):
        self.api = api
        self._data = kwargs
        self._data['token'] = token

    def __getattr__(self, field):
        if field in Job._VALID_FIELDS:
            if field == 'status':
                return self._data.get(field, 'unknown').lower()
            return self._data.get(field)
        else:
            return self.__getattribute__(field)

    @property
    def is_ready(self):
        return self.status == 'completed'

    @property
    def is_processing(self):
        return self.status in {'enqueued', 'processing'}

    @property
    def is_undefined(self):
        return self.status in {'unknown'}

    def __str__(self):
        return "Job {status}: {token}".format(status=self.status,
                                              token=self.token)

    @api_method
    def get_status(self):
        token = self.token
        response = self.api.request(
            endpoint="/jobs/%s" % token,
            data={
                "token": token,
            },
        )
        self._data.update(response.json())

    @api_method
    def wait_for_completion(self, timeout_seconds=None):
        printed_once = False
        max_end_date = datetime.datetime.utcnow() + datetime.timedelta(
            seconds=timeout_seconds
        ) if timeout_seconds else None

        if self.is_undefined:
            self.get_status()

        while True:
            if self.is_ready:
                break
            sleep(self._FILE_AVAILABILIY_SECONDS_DELAY)
            try:
                self.get_status()
            except APIException:  # keep waiting if API raises exceptions
                sleep(self._FILE_AVAILABILIY_SECONDS_DELAY)
                continue
            if max_end_date and datetime.datetime.utcnow() > max_end_date:
                raise DataFileTimeout(
                    "Timeout: job wasn't complete after %d seconds" % timeout_seconds
                )
            if not printed_once:
                logger.info("Waiting for the job to be ready...")
                printed_once = True

    @api_method
    def save_to_file(self, filename):
        api = self.api
        job = self  # just to be clear
        with open(filename, 'wb') as output:
            job.wait_for_completion()
            logger.info(u"Writing to %s" % filename)

            # this is a different request than the normal API
            # streaming the file in chunks
            r = requests.get(job.url,
                             headers=api.headers,
                             stream=True,
                             )

            for chunk in r.iter_content(chunk_size=self._CHUNK_SIZE):
                if chunk:
                    output.write(chunk)

    @api_method
    def iterate_results(self):
        api = self.api
        job = self  # just to be clear
        job.wait_for_completion()

        with requests.Session() as s:
            r = s.get(job.url,
                      headers=api.headers,
                      stream=True,
                      )
            iterator = r.iter_lines(chunk_size=self._CHUNK_SIZE)
            header = next(iterator)  # discard the header

            for line in iterator:
                yield line.decode('utf-8')
