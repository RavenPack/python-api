from ravenpackapi import RPApi


class TestDatafile(object):
    api = RPApi()

    def test_premium_url(self):
        premium_story_id = 'B5461869942657A8D4956BE409DEC944'
        url = self.api.get_document_url(
            premium_story_id
        )
        assert "ravenpack.com" in url

    def test_nonpremium_url(self):
        premium_story_id = '691D5D416F8E9752DDD9C2F8C30FBE53'
        url = self.api.get_document_url(
            premium_story_id
        )
        assert 'https://www.india.com/' in url
