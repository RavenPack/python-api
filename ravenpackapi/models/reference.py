import datetime

from ravenpackapi.utils.date_formats import as_date


class RPEntityMetadata(object):
    def __init__(self, value, start=None, end=None):
        super(RPEntityMetadata, self).__init__()
        self.value = value
        self.start = as_date(start)
        self.end = as_date(end)

    def is_valid(self, when=None):
        """ Check that the metadata is valid at the given time (default to now)"""
        if when is None:
            when = datetime.date.today()  # default to today
        when = as_date(when)

        if self.start and when < self.start:
            return False
        if self.end and when >= self.end:
            return False
        return True

    def __str__(self):
        return "Value: {value} - valid from {start} to {end}".format(
            **self.__dict__
        )


_MAPPED_FIELDS = {
    # the fields here are singular, we use the plural attributes
    # for returning a list of RPEntityMetadata
    "companies": "company",
    "countries": "country",
    "nationalities": "nationality",
    "validities": "validity",
}
_MAPPED_FIELDS.update(  # all regular plurals
    {"{}s".format(name): name for name in (
        'country_id', 'cusip', 'description',
        'name', 'entity_name',
        'geoname_id', 'government', 'has_member_id',
        'is_member_id', 'iso_code',
        'latitude', 'longitude',

        'isin', 'listing', 'mic', 'ticker',
        'organization_type', 'organization_type_id',
        'parent_org_id', 'parent_product_type',
        'parent_source', 'place_type', 'product_owner',
        'product_type', 'province', 'publication_type',
        'region_id', 'sedol', 'source_rank',
        'symbol', 'team_type', 'type',
    )}
)


class RpEntityReference(object):
    def __init__(self, rp_entity_id, data):
        super(RpEntityReference, self).__init__()
        self.rp_entity_id = rp_entity_id
        self._data = data

    def __getattr__(self, field):
        data_field = _MAPPED_FIELDS.get(field)
        if data_field:
            return [
                RPEntityMetadata(d['data_value'],
                                 d['range_start'],
                                 d['range_end'])
                for d in self._data[data_field]
            ]
        else:
            return self.__getattribute__(field)

    def __dir__(self):
        """ Help autocompleting this additional fields """
        return list(super(RpEntityReference, self).__dir__()) + [
            k for k in _MAPPED_FIELDS
        ]

    def __repr__(self):
        return "Reference for Entity {rp_entity_id}: {name}".format(
            rp_entity_id=self.rp_entity_id,
            name=self.names[-1].value
        )
