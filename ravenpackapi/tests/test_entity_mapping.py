from ravenpackapi import RPApi


class TestEntityMapping(object):
    api = RPApi()

    def test_matching_entity_mapping(self):
        entities = [{'ticker': 'AAPL', 'name': 'Apple Inc.'},
                    {'ticker': 'JPM'},
                    {'listing': 'XNYS:DVN'}]
        mapping = self.api.get_entity_mapping(entities)
        assert not mapping.errors
        assert len(mapping.matched) == len(mapping.submitted) == 3

        # let's get the first mapped entities
        rp_entity_ids = [match.id for match in mapping.matched]
        assert rp_entity_ids == ['D8442A', '619882', '14BA06']

    def test_mismatch_mapping(self):
        entities = ["unknown!"]
        mapping = self.api.get_entity_mapping(entities)
        rp_entity_ids = [match.id for match in mapping.matched]
        assert rp_entity_ids == []

    def test_mapping_example(self):
        invalid_entity_request = "Unknown entity specified"
        universe = [
            "RavenPack",
            {'ticker': 'AAPL'},
            'California, U.S.',
            {  # Amazon, specifying various fields
                "client_id": "12345-A",
                "date": "2017-01-01",
                "name": "Amazon Inc.",
                "entity_type": "COMP",
                "isin": "US0231351067",
                "cusip": "023135106",
                "sedol": "B58WM62",
                "listing": "XNAS:AMZN"
            },
            invalid_entity_request
        ]
        mapping = self.api.get_entity_mapping(universe)
        assert len(mapping.matched) == 4
        assert [m.name for m in mapping.matched] == [
            "RavenPack International S.L.",
            "Apple Inc.",
            "State of California, US",
            "Amazon.com Inc."
        ]
        assert len(mapping.errors) == 1
        assert mapping.errors[0].request == invalid_entity_request

    def test_matching_by_cusip(self):
        entities = [{'cusip': '037833100', },
                    {'cusip': '48127A161'},
                    {'cusip': '25179M103'}]
        api = self.api
        mapping = api.get_entity_mapping(entities)
        assert not mapping.errors
        assert len(mapping.matched) == len(mapping.submitted) == 3

    def test_multiple_candidates(self):
        entities = [
            {'isin': 'US88339J1051', 'name': 'TRADE DESK INC/THE -CLASS A'},
        ]
        api = self.api
        mapping = api.get_entity_mapping(entities)
        assert len(mapping.errors) == 1
        assert len(mapping.matched) == 0

        for close_match in mapping.errors:
            if close_match.candidates:
                best_match = close_match.candidates[0]
                assert best_match.id == '0E698B'
                assert best_match.name == 'The Trade Desk Inc.'
                assert best_match.type == 'comp'
            assert close_match.request == entities[0]
