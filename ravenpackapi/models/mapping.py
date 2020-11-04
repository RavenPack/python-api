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
        self.candidates = [
            RPMappingCandidate(candidate)
            for candidate in data.get('rp_entities', [])
        ]

        if not self.errors:
            # let's put the best candidate data on the obj for convenience
            best_match = self.candidates[0]
            self.id = best_match.id
            self.name = best_match.name
            self.type = best_match.type
            self.score = best_match.score


class RPMappingCandidate(object):
    def __init__(self, data):
        self.id = data['rp_entity_id']
        self.name = data['rp_entity_name']
        self.type = data['rp_entity_type']
        self.score = data['score']
