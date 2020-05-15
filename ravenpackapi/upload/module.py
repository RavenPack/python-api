import os

from ravenpackapi.upload.models import (File, FILE_FIELDS,
                                        Folder, FOLDER_FIELDS)
from ravenpackapi.utils.date_formats import as_datetime_str


class UploadApi(object):
    def __init__(self, api):
        self.api = api

    def list(self,
             start_date=None,
             end_date=None,
             tags=None,
             status=None,
             file_name=None,
             page_size=50,
             ):
        params = dict(
            start_date=as_datetime_str(start_date),
            end_date=as_datetime_str(end_date),
            tags=tags,
            status=status,
            file_name=file_name,
        )

        # the list of files is splitted in pages - let's collect them
        get_next, offset = False, 0
        while True:
            response = self.api.request('%s/files' % self.api._UPLOAD_BASE_URL,
                                        params={k: v
                                                for k, v in params.items()
                                                if v is not None})
            data = response.json()
            if 'results' in data:
                results = data['results']
                for r in results:
                    get_next = len(results) == page_size
                    file_params = {
                        field: r.get(field) for field in FILE_FIELDS
                    }
                    yield File(
                        api=self.api,
                        **file_params
                    )
            if not get_next:
                break
            offset += page_size
            params['offset'] = offset

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
        file_name = os.path.basename(filepath)

        params = dict(
            filename=file_name,
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
                    file_name=file_name)

    def get(self, file_id):
        return File(file_id, api=self.api)

    def list_folders(self):
        response = self.api.request('%s/folders' % self.api._UPLOAD_BASE_URL)
        data = response.json()
        for r in data:
            folder_params = {
                field: r.get(field) for field in FOLDER_FIELDS
            }
            yield Folder(**folder_params)

    def folder_get(self, folder_id):
        return Folder(folder_id, api=self.api)
