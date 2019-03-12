from ravenpackapi import RPApi

if __name__ == '__main__':
    entities = [{'ticker': 'AAPL', 'name': 'Apple Inc.'},
                {'ticker': 'JPM'},
                {'listing': 'XNYS:DVN'}]
    api = RPApi()

    mapping = api.get_entity_mapping(entities)

    # show the matched entities
    for match in mapping.matched:
        print(match.id, match.name, match.type, match.request)
