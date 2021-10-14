import logging
import mimetypes
import os
from time import sleep

from ravenpackapi.exceptions import APIException
from ravenpackapi.upload.models import (File, FILE_FIELDS,
                                        Folder, FOLDER_FIELDS)
from ravenpackapi.utils.date_formats import as_datetime_str

logger = logging.getLogger("ravenpack.upload")


class UploadApi(object):
    def __init__(self, api):
        self.api = api

    def list(self,
             start_date=None,
             end_date=None,
             tags=None,
             status=None,
             file_name=None,
             folder_id=None,
             page_size=50,
             ):
        params = dict(
            start_date=as_datetime_str(start_date),
            end_date=as_datetime_str(end_date),
            tags=tags,
            status=status,
            file_name=file_name,
            folder_id=folder_id,
            page_size=page_size,
        )

        # the list of files is splitted in pages - let's collect them
        get_next, offset = False, 0
        while True:
            response = self.api.request('%s/files' % self.api._UPLOAD_BASE_URL,
                                        params={k: v
                                                for k, v in params.items()
                                                if v is not None})
            data = response.json()
            results = data.get('results') or []
            get_next = len(results) == page_size
            for r in results:
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

    def file(self, name_or_file_handler,
             folder=None,
             source_url=None,
             properties=None,
             upload_mode=None):
        """ Upload a file - file can be either a file name or a file handler """
        close_file = False
        if source_url:
            if not isinstance(name_or_file_handler, str):
                raise ValueError("Please provide a filename together with the source_url parameter")
            filepath = name_or_file_handler
        else:
            if isinstance(name_or_file_handler, str):
                filepath = name_or_file_handler
                fh = open(filepath, 'rb')
                close_file = True
            else:
                filepath = name_or_file_handler.name
                fh = name_or_file_handler
        file_name = os.path.basename(filepath)

        if isinstance(folder, Folder):
            folder_id = folder.folder_id
        else:
            folder_id = folder

        params = dict(
            file_name=file_name,
            properties=properties,
            folder_id=folder_id,
            source_url=source_url,
            upload_mode=upload_mode,
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

        if source_url is None:
            # 2 steps upload - we now go and upload via the PUT method
            location = promise['Location']
            content_type = mimetypes.guess_type(file_name)[0]
            attempt = 3
            while attempt:
                try:
                    fh.seek(0)
                    self.api.request(
                        endpoint=location,
                        method='put',
                        data=fh,
                        headers={
                            "x-amz-server-side-encryption": "AES256",
                            "Content-Type": content_type,
                        }
                    )
                except APIException as e:
                    attempt -= 1
                    if attempt == 0:
                        raise e  # raise the exception
                    logger.warning("Error with PUT file operation - retring")
                    sleep(1)
                else:
                    break

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
        for r in data['results']:
            folder_params = {
                field: r.get(field) for field in FOLDER_FIELDS
            }
            yield Folder(**folder_params)

    def folder_get(self, folder_id):
        return Folder(folder_id, api=self.api)

    def folder_create(self, folder_name, parent_folder_id=None, starred=False, trashed=False):
        folder = Folder(folder_id=None,
                        folder_name=folder_name,
                        parent_folder_id=parent_folder_id,
                        starred=starred, trashed=trashed,
                        api=self.api)
        folder.save()
        return folder

    def quota(self):
        response = self.api.request('%s/quota' % self.api._UPLOAD_BASE_URL)
        return response.json()
