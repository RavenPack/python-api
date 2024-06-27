import logging

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from ravenpackapi.exceptions import APIException425

logger = logging.getLogger("ravenpack.upload.retry")


def retry_on_too_early(func, *args, **kwargs):
    """
    Retry a function that may raise a 425 API exception.

    Note: This was originally implemented using the library "retry" and migrated
    to tenacity. It should not be used in new code, as the proper way to do this
    using tenacity is to decorate the funciton with @retry.
    """
    wrapped_func = retry(
        retry=retry_if_exception_type(APIException425),
        wait=wait_exponential_jitter(initial=3, exp_base=2, jitter=5),
        stop=stop_after_attempt(10),
        reraise=True,
    )(func)
    return wrapped_func(*args, **kwargs)
