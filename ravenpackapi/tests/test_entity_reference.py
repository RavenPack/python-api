from ravenpackapi import RPApi
from ravenpackapi.exceptions import APIException

APPLE_RP_ENTITY_ID = 'D8442A'


class TestEntityReference():
    api = RPApi()

    def test_alphabet(self):
        reference = self.api.get_entity_reference(APPLE_RP_ENTITY_ID)

        assert reference.rp_entity_id == APPLE_RP_ENTITY_ID
        assert reference.names[-1].value == 'APPLE INC.'
        assert reference.tickers[-1].value == 'AAPL'

    def test_failing(self):
        try:
            missing = self.api.get_entity_reference('invalid')
            assert False, "Invalid entity should raise an Exception"
        except APIException:
            pass
