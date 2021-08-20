import datetime
import io
import os
import tempfile

import pytest

from ravenpackapi import RPApi
from ravenpackapi.exceptions import APIException
from ravenpackapi.models.reference import RPEntityMetadata

APPLE_RP_ENTITY_ID = 'D8442A'


class TestEntityReference(object):
    api = RPApi()

    def test_apple(self):
        reference = self.api.get_entity_reference(APPLE_RP_ENTITY_ID)

        assert reference.rp_entity_id == APPLE_RP_ENTITY_ID
        assert reference.names[-1].value == reference.name == 'APPLE INC.'
        assert reference.tickers[-1].value == 'AAPL'

    def test_failing(self):
        try:
            missing = self.api.get_entity_reference('invalid')
            assert False, "Invalid entity should raise an Exception"
        except APIException:
            pass


class TestMetadataValidity(object):
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


class TestEntityTypeReference(object):
    api = RPApi()
    team_reference = api.get_entity_type_reference('team')

    @pytest.mark.slow
    @pytest.mark.parametrize("date", [None, datetime.date(2017, 8, 2)])
    def test_save_team_reference(self, date):
        """ Get the team reference as a CSV """

        team_reference = self.api.get_entity_type_reference('team', date=date)
        f = tempfile.NamedTemporaryFile(prefix='test_reference', delete=False)
        filepath = f.name
        team_reference.write_to_file(filepath)

        with io.open(filepath, encoding='latin-1') as f:
            lines = f.readlines()
            assert len(lines) > 100, "We should have several rows"
            assert lines[0] == 'RP_ENTITY_ID,ENTITY_TYPE,DATA_TYPE,DATA_VALUE,RANGE_START,RANGE_END\n'
        os.unlink(f.name)

    def test_team_reference_as_map(self):
        club = self.team_reference['022568']
        assert club.name == 'Olympique de Marseille'

    def test_team_iterate_entities(self):
        valid_entities = set()
        for entity in self.team_reference:
            last_name = entity.entity_names[-1]
            if last_name.is_valid():
                valid_entities.add(entity.rp_entity_id)

        assert len(valid_entities) > 100, "We should have several valid teams"
