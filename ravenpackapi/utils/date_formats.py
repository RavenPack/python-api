import datetime

from six import string_types

from ravenpackapi.exceptions import ValidationError

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

ALLOWED_DATETIME_FORMATS = (
    "%Y-%m-%d %H:%M:%S.%f",
    '%Y-%m-%d',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M'
)


def as_date(s):
    if not s:  # the date on CSV files is an empty string
        return None
    if isinstance(s, string_types):
        s = s.strip()
        return datetime.datetime.strptime(s, DATE_FORMAT).date()
    return s


def as_datetime(s):
    if isinstance(s, str):
        s = s.strip()
        for format in ALLOWED_DATETIME_FORMATS:
            try:
                return datetime.datetime.strptime(s, format)
            except ValueError:
                pass
        raise ValidationError(
            "Invalid date: '%s', please pass a datetime or a string format" % s
        )
    return s


def from_timestamp(s):
    return datetime.datetime.strptime(s, TIMESTAMP_FORMAT)


def as_datetime_str(s):
    if isinstance(s, datetime.date):
        return s.strftime(DATETIME_FORMAT)
    return s


def as_date_str(s):
    if isinstance(s, datetime.date):
        return s.strftime(DATE_FORMAT)
    return s
