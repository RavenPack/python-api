import csv
import logging
import sys

import six
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MO

from ravenpackapi.utils.date_formats import as_datetime

SPLIT_YEARLY = 'yearly'
SPLIT_MONTHLY = 'monthly'
SPLIT_WEEKLY = 'weekly'
SPLIT_DAILY = 'daily'
logger = logging.getLogger("ravenpack.util")


def parts_to_curl(method, endpoint, headers, data=None):
    ignored_headers = (
        'Accept', 'Accept-Encoding', 'Connection',
        'Content-Type', 'Content-Length', 'User-Agent'
    )
    headers = ["'{0}:{1}'".format(k, v) for k, v in headers.items() if
               k not in ignored_headers]
    headers = " -H ".join(sorted(headers))

    curl_parameters = ['curl']
    for prefix, values in (('-X', method.upper()),
                           ('-H', headers),
                           ('-d', "'%s'" % data if data else None),
                           ):
        if values:
            curl_parameters.append('%s %s' % (prefix, values))
    curl_parameters.append("'%s'" % endpoint)
    command = " ".join(curl_parameters)
    return command


def to_curl(request):
    if not request:
        return 'No request'
    try:
        data = request.body.decode() if getattr(request, 'body') else None
    except Exception as e:
        logger.debug("Cannot convert data to curl: %s" % e)
        data = "?"
    return parts_to_curl(request.method,
                         request.url,
                         request.headers,
                         data=data)


def time_intervals(date_start, date_end, split=SPLIT_MONTHLY):
    assert split in (
        SPLIT_YEARLY,
        SPLIT_MONTHLY,
        SPLIT_WEEKLY,
        SPLIT_DAILY)
    start = as_datetime(date_start)
    date_end = as_datetime(date_end)

    def get_end(get_next_end):
        if split == SPLIT_MONTHLY:
            # up to beginning of next month
            return get_next_end + \
                   relativedelta(
                       months=+1,
                       day=1, hour=0, minute=0, second=0, microsecond=0
                   )
        elif split == SPLIT_YEARLY:
            # up to beginning of next year
            return get_next_end + \
                   relativedelta(
                       years=+1,
                       month=1, day=1, hour=0, minute=0, second=0, microsecond=0
                   )
        elif split == SPLIT_WEEKLY:
            # will break the time on weeks starting on Mondays
            return get_next_end + \
                   relativedelta(
                       days=+1, weekday=MO,
                       hour=0, minute=0, second=0, microsecond=0
                   )
        elif split == SPLIT_DAILY:
            # will break the time on weeks starting on Mondays
            return get_next_end + \
                   relativedelta(
                       days=+1,
                       hour=0, minute=0, second=0, microsecond=0
                   )

    while True:
        # some datetime trick to get the beginning of next month
        end = min(date_end, get_end(start))
        if start >= date_end:
            break
        yield start, end
        start = end


def parse_csv_line(line):
    """ Decode a line of CSV
        line is unicode
    """
    if sys.version_info[0] < 3:
        if isinstance(line, six.text_type):
            line = line.encode('utf-8')  # Python 2 wants utf8 bytes
    else:
        if not isinstance(line, six.text_type):
            line = line.decode('utf-8')  # Python 3 wants strings
    return list(csv.reader((line,)))[0]
