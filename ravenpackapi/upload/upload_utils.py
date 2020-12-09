import logging

from retry.api import retry_call

from ravenpackapi.exceptions import APIException404

logger = logging.getLogger('ravenpack.upload.retry')


def retry_404(func, *args, **kwargs):
    response = retry_call(func, fargs=args, fkwargs=kwargs,
                          exceptions=(APIException404,),
                          delay=3, backoff=2, jitter=(1, 5), tries=10,
                          logger=logger)
    return response
