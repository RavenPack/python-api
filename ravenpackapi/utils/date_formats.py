import datetime


def as_date(s):
    if isinstance(s, str):
        return datetime.datetime.strptime(s, '%Y-%m-%d').date()
    return s
