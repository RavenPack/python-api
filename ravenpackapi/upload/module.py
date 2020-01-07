import json
import os

from ravenpackapi.upload.models import File
from ravenpackapi.utils.date_formats import as_datetime_str


class UploadApi(object):
    def __init__(self, api):
        self.api = api

    def list(self,
             start_date=None,
             end_date=None,
             tags=None,
             status=None,
             filename=None,
             ):
        params = dict(
            start_date=as_datetime_str(start_date),
            end_date=as_datetime_str(end_date),
            tags=tags,
            status=status,
            filename=filename,
        )

        # the list of files is splitted in pages - let's collect them
        while True:
            response = self.api.request('%s/files' % self.api._UPLOAD_BASE_URL,
                                        params={k: v
                                                for k, v in params.items()
                                                if v is not None})
            data = response.json()
            if 'results' in data:
                for r in data['results']:
                    yield File(r['file_id'],
                               status=r.get('status'),
                               name=r.get('name'),
                               api=self.api,
                               )
            if data.get('next_page_key'):  # next page
                params['next_page_key'] = json.dumps(data['next_page_key'])
            else:
                break

    def file(self, name_or_file_handler, properties=None):
        """ Upload a file - file can be either a filename or a file handler """
        close_file = False
        if isinstance(name_or_file_handler, str):
            filepath = name_or_file_handler
            fh = open(filepath, 'rb')
            close_file = True
        else:
            filepath = name_or_file_handler.name
            fh = name_or_file_handler
        filename = os.path.basename(filepath)

        params = dict(
            filename=filename,
            properties=properties
        )

        first_response = self.api.request(
            endpoint='%s/files' % self.api._UPLOAD_BASE_URL,
            method='post',
            json={k: v
                  for k, v in params.items()
                  if v is not None},
        )

        promise = first_response.json()
        file_id = promise['file_id']
        location = promise['Location']

        self.api.request(
            endpoint=location,
            method='put',
            data=fh,
            headers={
                "x-amz-server-side-encryption": "AES256",
            }
        )

        if close_file:  # we opened the handler, so let's close it
            fh.close()
        return File(file_id,
                    api=self.api,
                    name=filename)

    def get(self, file_id):
        return File(file_id, api=self.api)
