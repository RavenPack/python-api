from ravenpackapi import RPApi


class TestUploadFlow:
    api = RPApi()

    def test_quota(self):
        data = self.api.upload.quota()
        for field in ('files', 'quota'):
            assert field in data
