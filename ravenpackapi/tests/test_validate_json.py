from ravenpackapi.models.results import Result

analytics = {
    'TIMESTAMP_UTC': '2018-03-05 16:17:19.047',
    'RP_STORY_ID': '5E2E050D393D9A059383F62A80F6EA86',
    'RP_ENTITY_ID': '6203E4',
    'ENTITY_TYPE': 'COMP',
    'ENTITY_NAME': 'Time Warner Inc.',
    'COUNTRY_CODE': 'US',
    'RELEVANCE': 8,
    'EVENT_SENTIMENT_SCORE': None,
    'EVENT_RELEVANCE': None,
    'EVENT_SIMILARITY_KEY': None,
    'EVENT_SIMILARITY_DAYS': None,
    'TOPIC': None,
    'GROUP': None, 'TYPE': None,
    'SUB_TYPE': None, 'PROPERTY': None, 'FACT_LEVEL': None,
    'RP_POSITION_ID': None, 'POSITION_NAME': None, 'EVALUATION_METHOD': None,
    'MATURITY': None, 'EARNINGS_TYPE': None, 'EVENT_START_DATE_UTC': None,
    'EVENT_END_DATE_UTC': None, 'REPORTING_PERIOD': None, 'REPORTING_START_DATE_UTC': None,
    'REPORTING_END_DATE_UTC': None, 'RELATED_ENTITY': None, 'RELATIONSHIP': None,
    'CATEGORY': None, 'EVENT_TEXT': None, 'NEWS_TYPE': 'PRESS-RELEASE',
    'RP_SOURCE_ID': 'FFD30D', 'SOURCE_NAME': 'Business Wire (Online)', 'CSS': 0.0,
    'NIP': -0.18, 'PEQ': 0, 'BEE': 0, 'BMQ': 0, 'BAM': 0, 'BCA': 0, 'BER': 0, 'ANL_CHG': 0,
    'MCQ': 0, 'RP_STORY_EVENT_INDEX': 2, 'RP_STORY_EVENT_COUNT': 6, 'PRODUCT_KEY': 'RPA',
    'PROVIDER_ID': 'MRVR', 'PROVIDER_STORY_ID': '10:33477848749',
    'HEADLINE': 'Orlando Jones Joins BANDWAGON Board'
}


class TestValidResult(object):
    def test_valid_from_obj(self):
        r = Result(analytics)
        assert r.is_invalid is False
