import datetime
import io
import logging
from operator import itemgetter

from ravenpackapi.util import parse_csv_line
from ravenpackapi.utils.date_formats import as_date

logger = logging.getLogger('ravenpack.reference')


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
    def __init__(self, rp_entity_id, data, entity_type=None):
        super(RpEntityReference, self).__init__()
        self.rp_entity_id = rp_entity_id
        self._data = data
        self.type = entity_type

    def __getattr__(self, field):
        data_field = _MAPPED_FIELDS.get(field)
        if data_field:
            metadata_records = self._data.get(data_field, [])
            metadata_records.sort(key=itemgetter('range_start'))
            return [
                RPEntityMetadata(d['data_value'],
                                 d['range_start'],
                                 d['range_end'])
                for d in metadata_records
            ]
        else:
            return self.__getattribute__(field)

    def __dir__(self):
        """ Help autocompleting this additional fields """
        return list(super(RpEntityReference, self).__dir__()) + [
            k for k in _MAPPED_FIELDS
        ]

    @property
    def name(self):
        names = self.names or self.entity_names
        return names[-1].value if names else None

    def __repr__(self):
        return "Reference for Entity {rp_entity_id}: {name}".format(
            rp_entity_id=self.rp_entity_id,
            name=self.name
        )


class EntityTypeReference(object):
    """ An object getting the references of many entities from a file """

    def __init__(self, http_response=None, file_path=None):
        super(EntityTypeReference, self).__init__()
        self.parse_start = self.parse_end = False
        self.http_response = http_response
        self.file_path = file_path
        self._entities = {}
        assert http_response or file_path, "Please provide one source"

    def _iter_rows(self):
        if self.parse_start:
            raise Exception("Reference file can be iterated only once")
        self.parse_start = True
        if self.http_response:
            lines = self.http_response.iter_lines(decode_unicode=True)
            for line in lines:
                yield line
        elif self.file_path:
            with io.open(self.file_path, encoding='latin-1') as f:
                for line in f.readlines():
                    yield line
        self.parse_end = True

    def _parse_lines(self):
        iterator = self._iter_rows()
        headers = next(iterator)
        yield headers
        for line in iterator:
            parsed_line = parse_csv_line(line)
            rp_entity_id, entity_type, data_type, data_value, range_start, range_end = parsed_line
            if rp_entity_id not in self._entities:
                self._entities[rp_entity_id] = entity = RpEntityReference(rp_entity_id, {},
                                                                          entity_type=entity_type)
            else:
                entity = self._entities[rp_entity_id]
            data_type = data_type.lower()
            if data_type not in entity._data:
                entity._data[data_type] = []
            entity._data[data_type].append(dict(
                data_value=data_value,
                range_start=range_start,
                range_end=range_end
            ))

            yield line

    def _parse(self):
        for line in self._parse_lines():
            pass

    def write_to_file(self, filename):
        """ This will consume the lines and write them to disk
            This can be done only before the first iteration
        """
        logger.info("Writing Entity reference to %s" % filename)
        with io.open(filename, 'w', encoding='latin-1') as output:
            for line in self._parse_lines():
                output.write(line + '\n')

    def __getitem__(self, rp_entity_id):
        if not self.parse_end:
            self._parse()
        return self._entities[rp_entity_id]

    def __iter__(self):
        # parse the entities and return them ordered by rp_entity_id
        if not self.parse_end:
            self._parse()

        keys = list(self._entities.keys())
        keys.sort()
        for rp_entity_id in keys:
            yield self._entities[rp_entity_id]
