from time import sleep

from ravenpackapi.exceptions import api_method

FILE_FIELDS = (
    'file_id', 'file_name', 'folder_id',
    'status',
    'upload_ts', 'raw_size', 'starred', 'trashed',
    'tags',
)

FOLDER_FIELDS = (
    'folder_id', 'parent_folder_id',
    'folder_name',
    'starred', 'trashed',
)


class File(object):
    """ A promise to get a file """

    # check FILE_FIELD for the supported fields
    def __init__(self, file_id,
                 file_name=None, folder_id=None,
                 status=None,
                 upload_ts=None, raw_size=None, starred=None, trashed=None,
                 tags=None,
                 api=None,
                 ):
        self.api = api
        self.file_id = file_id
        self.folder_id = folder_id
        self.tags = tags or []
        self.status = status

        self.upload_ts = upload_ts
        self.starred = starred
        self.trashed = trashed
        self.raw_size = raw_size
        self.file_name = file_name

    def __str__(self):
        self.get_metadata()  # be sure to have the metadata (this is called only once per file)
        return "File: %(file_id)s - %(file_name)s - status: %(status)s" % self.__dict__

    @api_method
    def get_status(self):
        response = self.api.request('%s/files/%s/status' % (self.api._UPLOAD_BASE_URL, self.file_id))
        self.status = response.json()['status']
        return self.status

    @api_method
    def get_metadata(self, force_refresh=False):
        if self.file_name and not force_refresh:  # we already have the file metadata
            return
        response = self.api.request('%s/files/%s/metadata' % (self.api._UPLOAD_BASE_URL, self.file_id))
        metadata = response.json()
        for field in FILE_FIELDS:
            setattr(self, field, metadata.get(field))

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
    def set_metadata(self, file_name=None,
                     folder_id=None,
                     trashed=None, starred=None,
                     tags=None
                     ):
        metadata = {k: v
                    for k, v in dict(file_name=file_name, folder_id=folder_id,
                                     trashed=trashed, starred=starred, tags=tags,
                                     ).items()
                    if v is not None}
        self.api.request('%s/files/%s/metadata' % (self.api._UPLOAD_BASE_URL, self.file_id),
                         json=metadata,
                         method='patch')

    def wait_for_completion(self):
        while self.status not in {"COMPLETED", "DELETED"}:
            sleep(1)
            self.get_status()


class Folder(object):
    """ A Folder containing files """

    def __init__(self, folder_id,
                 folder_name=None,
                 parent_folder_id=None,
                 starred=None, trashed=None,
                 api=None,
                 ):
        self.api = api
        self.folder_id = folder_id
        self.parent_folder_id = parent_folder_id
        self.folder_name = folder_name

        self.starred = starred
        self.trashed = trashed

    def __str__(self):
        return "Folder: %(folder_id)s - %(folder_name)s" % self.__dict__

    @api_method
    def delete(self):
        response = self.api.request('%s/folder/%s' % (self.api._UPLOAD_BASE_URL, self.folder_id),
                                    method='delete')
        return response

    @api_method
    def set_metadata(self,
                     folder_name=None,
                     parent_folder_id=None,
                     trashed=None, starred=None,
                     ):
        metadata = {k: v
                    for k, v in dict(folder_name=folder_name,
                                     parent_folder_id=parent_folder_id,
                                     trashed=trashed, starred=starred,
                                     ).items()
                    if v is not None}
        self.api.request('%s/folders/%s' % (self.api._UPLOAD_BASE_URL, self.folder_id),
                         json=metadata,
                         method='patch')
