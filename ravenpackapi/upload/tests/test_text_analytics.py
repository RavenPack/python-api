import os

from ravenpackapi import RPApi


class TestRecentAnalyticsRetried:
    api = RPApi()

    def test_upload_delete_retry(self):
        """ When we delete immediately after creation we get a 404
            The API should silently retry for some time
        """
        api = self.api
        filename = "upload_sample.txt"
        f = api.upload.file(os.path.join(os.path.dirname(__file__), filename))
        f.delete()
