from decimal import Decimal

from ravenpackapi.utils.date_formats import from_timestamp


class Field(object):
    def __init__(self, name, field_type=str, validators=None):
        """
        :type field_type: (Callable[[str], object])
        """
        self.name = name.upper()
        self.field_type = field_type
        self.validators = validators if validators is not None else []

    def get(self, value):
        return self.field_type(value)

    def __repr__(self):
        return '<Field: %s>' % self.name

    def validate(self, value):
        for validator in self.validators:
            if not validator(value):
                return False
        return True


def length_is(length):
    return lambda value: value is None or len(value) == length


def less_or_equal_than(max):
    return lambda value: value is None or value <= max


def str_optional(value):
    if value is not None:
        return str(value)
    return None


def decimal_optional(value):
    if value is not None:
        return Decimal(value)
    return None


def int_optional(value):
    if value is not None:
        return int(value)
    return None


ANALYTICS_FIELDS = [
    Field('timestamp_utc', from_timestamp),
    Field('rp_story_id', str),

    Field('rp_entity_id', str, validators=[length_is(6)]),
    Field('entity_type', str, validators=[length_is(4)]),
    Field('entity_name', str),

    Field('country_code', str, validators=[length_is(2)]),
    Field('relevance', int, validators=[less_or_equal_than(100)]),
    Field('event_sentiment_score', decimal_optional),
    Field('event_relevance', decimal_optional),

    Field('event_similarity_key', str_optional),
    Field('event_similarity_days', int_optional),

    Field('topic', str_optional),
    Field('group', str_optional),
    Field('type', str_optional),
    Field('sub_type', str_optional),
    Field('property', str_optional),
    Field('fact_level', str_optional),
    Field('rp_position_id', str_optional),
    Field('position_name', str_optional),
    Field('evaluation_method', str_optional),
    Field('maturity', str_optional),
    Field('earnings_type', str_optional),

    Field('event_start_date_utc', str_optional),
    Field('event_end_date_utc', str_optional),
    Field('reporting_period', str_optional),
    Field('reporting_start_date_utc', str_optional),
    Field('reporting_end_date_utc', str_optional),
    Field('related_entity', str_optional),
    Field('relationship', str_optional),

    Field('category', str_optional),
    Field('event_text', str_optional),
    Field('news_type', str_optional),
    Field('rp_source_id', str_optional),
    Field('source_name', str_optional),

    Field('css', float),
    Field('nip', float),
    Field('peq', int),
    Field('bee', int),
    Field('bmq', int),
    Field('bam', int),
    Field('bca', int),
    Field('ber', int),

    Field('anl_chg', int),
    Field('mcq', int),
    Field('rp_story_event_index', int),
    Field('rp_story_event_count', int),

    Field('product_key', str),
    Field('provider_id', str),
    Field('provider_story_id', str),

    Field('headline', str),
]

ANALYTICS_FIELDS_SET = set(
    [f.name for f in ANALYTICS_FIELDS]
)

FIELD_MAP = {
    f.name: f for f in ANALYTICS_FIELDS
}
