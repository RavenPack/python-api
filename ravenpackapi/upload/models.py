import json
from time import sleep

from ravenpackapi.exceptions import api_method


class File(object):
    """ A promise to get a file """

    def __init__(self, file_id,
                 status=None,
                 name=None,
                 api=None,
                 ):
        self.file_id = file_id
        self.status = status
        self.name = name
        self.api = api

    def __str__(self):
        return "File: %(file_id)s - %(name)s - status: %(status)s" % self.__dict__

    @api_method
    def get_status(self):
        response = self.api.request('%s/files/%s/status' % (self.api._UPLOAD_BASE_URL, self.file_id))
        self.status = response.json()['status']
        return self.status

    @api_method
    def save_original(self, filename):
        response = self.api.request('%s/files/%s' % (self.api._UPLOAD_BASE_URL, self.file_id),
                                    stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=self.api._CHUNK_SIZE):
                f.write(chunk)

    @api_method
    def save_analytics(self, filename, output_format='application/json'):
        response = self.api.request('%s/files/%s/analytics' % (self.api._UPLOAD_BASE_URL, self.file_id,),
                                    headers=dict(
                                        Accept=output_format,
                                        **self.api.headers
                                    ),
                                    stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=self.api._CHUNK_SIZE):
                f.write(chunk)

    @api_method
    def save_annotated(self, filename):
        response = self.api.request('%s/files/%s/annotated' % (self.api._UPLOAD_BASE_URL, self.file_id),
                                    stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=self.api._CHUNK_SIZE):
                f.write(chunk)

    @api_method
    def delete(self):
        response = self.api.request('%s/files/%s' % (self.api._UPLOAD_BASE_URL, self.file_id),
                                    method='delete')
        return response

    @api_method
    def set_tags(self, tags):
        self.api.request('%s/files/%s/tags' % (self.api._UPLOAD_BASE_URL, self.file_id),
                         data=json.dumps(tags),
                         method='put')

    def wait_for_completion(self):
        while self.status not in {"COMPLETED", "DELETED"}:
            sleep(1)
            self.get_status()
