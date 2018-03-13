class RPMappingResults(object):
    def __init__(self, data):
        self.errors = []
        self.matched = []
        self.submitted = []
        for mapping in data['identifiers_mapped']:
            match = RPMappingMatch(mapping)
            self.submitted.append(match)
            if match.errors:
                self.errors.append(match)
            else:
                self.matched.append(match)


class RPMappingMatch(object):
    def __init__(self, data):
        self.request = data['request_data']
        self.errors = data['errors']
        if not self.errors:
            self.candidates = data['rp_entities']
            # let's put the best candidate data on the obj for convenience
            best_match = self.candidates[0]
            self.id = best_match['rp_entity_id']
            self.name = best_match['rp_entity_name']
            self.type = best_match['rp_entity_type']
