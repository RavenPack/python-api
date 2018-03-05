import datetime

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DATE_FORMAT = '%Y-%m-%d'


def as_date(s):
    if isinstance(s, str):
        return datetime.datetime.strptime(s, DATE_FORMAT).date()
    return s


def from_timestamp(s):
    return datetime.datetime.strptime(s, TIMESTAMP_FORMAT)
