import logging

import pytest

from ravenpackapi import RPApi
from ravenpackapi.models.results import Result

logger = logging.getLogger('ravenpack.test.realtime_feed')


class TestRealtimeFeed():
    api = RPApi()

    @pytest.mark.slow
    def test_get_something_from_us500(self, dataset='us500',
                                      max_received=5):
        ds = self.api.get_dataset(dataset_id=dataset)

        received = 0
        for record in ds.request_realtime():
            assert isinstance(record, Result)
            received += 1
            logger.info("Got {received}/{max} from us500".format(
                received=received, max=max_received
            ))
            errors = record.is_invalid
            assert errors is False, 'Record is invalid: %s' % errors
            if received > max_received:
                break
