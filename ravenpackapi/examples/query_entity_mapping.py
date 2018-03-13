from ravenpackapi import RPApi


class TestEntityMapping(object):
    api = RPApi()

    def test_matching_entity_mapping(self):
        entities = [{'ticker': 'AAPL', 'name': 'Apple Inc.'},
                    {'ticker': 'JPM'},
                    {'listing': 'XNYS:DVN'}]
        api = self.api
        mapping = api.get_entity_mapping(entities)
        assert not mapping.errors
        assert len(mapping.matched) == len(mapping.submitted) == 3

        # let's get the first mapped entities
        rp_entity_ids = [match.id for match in mapping.matched]
        assert rp_entity_ids == ['D8442A', '619882', '14BA06']

    def test_mismatch_mapping(self):
        entities = ["unknown!"]
        api = self.api
        mapping = api.get_entity_mapping(entities)
        rp_entity_ids = [match.id for match in mapping.matched]
        assert rp_entity_ids == []
