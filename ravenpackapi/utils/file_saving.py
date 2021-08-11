import logging

from ravenpackapi.exceptions import APIException
from ravenpackapi.util import to_curl

logger = logging.getLogger(__name__)


def save_stream_response(response, filename, chunk_size=8192):
    if response.status_code != 200:
        logger.error("Error calling the API, we tried: %s" % to_curl(response.request))
        raise APIException(
            'Got an error {status}: body was \'{error_message}\''.format(
                status=response.status_code, error_message=response.text
            ), response=response)

    logger.info(u"Writing to %s" % filename)
    with open(filename, "wb") as output:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                output.write(chunk)
