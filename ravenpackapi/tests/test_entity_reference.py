import datetime

from ravenpackapi import RPApi
from ravenpackapi.exceptions import APIException
from ravenpackapi.models.reference import RPEntityMetadata

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


class TestMetadataValidity():
    def test_specific_valid_range(self):
        md = RPEntityMetadata('year 1990',
                              start=datetime.date(1990, 1, 1),
                              end=datetime.date(1991, 1, 1))
        assert md.is_valid(when='1990-06-01')
        assert not md.is_valid(when='1991-01-01')
        assert not md.is_valid(when='1989-12-31')

    def test_open_end(self):
        md = RPEntityMetadata('since 1990',
                              start=datetime.date(1990, 1, 1),
                              )
        assert not md.is_valid(when='1989-12-31')
        assert md.is_valid(when='1990-06-01')
        assert md.is_valid(when='1991-01-01')

    def test_open_start(self):
        md = RPEntityMetadata('until 1990',
                              end=datetime.date(1991, 1, 1),
                              )
        assert md.is_valid(when='1989-12-31')
        assert md.is_valid(when='1990-06-01')
        assert not md.is_valid(when='1991-01-01')

    def test_always_valid(self):
        md = RPEntityMetadata('always valid')
        assert md.is_valid(when='1989-12-31')
        assert md.is_valid(when='1990-06-01')
        assert md.is_valid(when='1991-01-01')
