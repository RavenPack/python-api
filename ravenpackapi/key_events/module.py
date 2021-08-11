import os

from ravenpackapi.utils.file_saving import save_stream_response


class KeyEventsApi(object):
    def __init__(self, api, product):
        self.api = api
        self.product = product

    def _request_list(self, file_type):

        response = self.api.request(
            "/%s/history/%s/" % (self.product, file_type)
        )
        data = response.json()
        return data

    def list_yearly_archives(self):
        return self._request_list('yearly')

    def list_daily_files(self):
        return self._request_list('daily')

    def list_reference_files(self):
        return self._request_list('reference')

    def download_file(self, file_id, filename=None):
        if file_id.startswith("/"):
            url = file_id
            if filename is None:
                filename = os.path.basename(file_id)
        else:
            # the id is the filename - we can get the url from there
            if file_id.endswith(".zip"):
                file_type = "yearly"
            elif "-reference." in file_id:
                file_type = "reference"
            else:
                file_type = "daily"
            url = "/%(product)s/file/%(file_type)s/%(id)s" % {
                "product": self.product,
                "file_type": file_type,
                "id": file_id
            }
            if filename is None:
                filename = file_id
        response = self.api.session.get(self.api._BASE_URL + url,
                                        headers=self.api.headers,
                                        stream=True,
                                        **self.api.common_request_params
                                        )
        save_stream_response(response, filename=filename)
