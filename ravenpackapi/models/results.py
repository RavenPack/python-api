import json
from collections import OrderedDict

from past.builtins import basestring

from ravenpackapi.models.fields import ANALYTICS_FIELDS_SET, FIELD_MAP, ANALYTICS_FIELDS


class Results(object):
    def __init__(self, data, name=None):
        self._data = data
        self.name = name

    @property
    def description(self):
        result = self.name + ". " if self.name else ""
        result += "%d records" % len(self._data)
        return result

    def __str__(self):
        return "Results %s" % self.description

    def __iter__(self):
        return self._data.__iter__()

    def __nonzero__(self):
        return bool(self._data)

    def __len__(self):
        return len(self._data)


class Result(object):
    def __init__(self, record):
        if isinstance(record, basestring):
            self.data = json.loads(record)
        else:
            self.data = record

    def __str__(self):
        typed_object = OrderedDict(
            [(field.name, field.get(self.data[field.name])) for field in ANALYTICS_FIELDS]
        )
        return str(typed_object)

    def __getattr__(self, field):
        normalized_field = field.upper()
        analytics_field = FIELD_MAP.get(normalized_field)
        if analytics_field is None:
            return self.__getattribute__(field)

        return analytics_field.get(self.data[normalized_field])

    def __getitem__(self, item):
        normalized_field = item.upper()
        return getattr(self, normalized_field)

    @property
    def is_invalid(self):
        errors = []
        for field in ANALYTICS_FIELDS_SET:
            value = getattr(self, field)
            field = FIELD_MAP[field]
            if not field.validate(value):
                errors.append(field)
        return errors or False
