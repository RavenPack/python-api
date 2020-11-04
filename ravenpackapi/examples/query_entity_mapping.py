from ravenpackapi import RPApi

if __name__ == '__main__':
    entities = [
        {'ticker': 'AAPL', 'name': 'Apple Inc.'},
        {'ticker': 'JPM'},
        {'listing': 'XNYS:DVN'},

        # this won't match with confidence
        {'isin': 'US88339J1051', 'name': 'TRADE DESK INC/THE -CLASS A'},
    ]
    api = RPApi()

    mapping = api.get_entity_mapping(entities)

    # show the matched entities
    for match in mapping.matched:
        print(match.id, match.name, match.type, match.score, match.request)

    for close_match in mapping.errors:
        if close_match.candidates:
            best_match = close_match.candidates[0]
            print(best_match.id, best_match.name, best_match.type, best_match.score, close_match.request)
