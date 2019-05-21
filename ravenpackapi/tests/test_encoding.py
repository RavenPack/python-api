import pytest

from ravenpackapi import RPApi, Dataset


class TestEncoding(object):
    api = RPApi()
    ds = None

    @classmethod
    def setup_class(cls):
        cls.ds = cls.api.create_dataset(
            Dataset(
                name='testing_encoding',
                filters={
                    "rp_entity_id": '9BFEB5'  # this entity has non-ascii name
                },
            )
        )

    params = dict(
        start_date='2018-05-01 21:51',  # we have an event here
        end_date='2018-05-01 21:52',
    )

    @pytest.mark.json
    def test_json_iterate(self):
        self.api.log_curl_commands = True

        results = self.ds.json(
            **self.params
        )
        assert results, 'We should have some result in the timerange'
        for analytic_row in results:
            print(analytic_row)

    def test_dump_iterate(self):
        results = self.ds.request_datafile(
            **self.params
        )
        for analytic_row in results:
            print(analytic_row)

    @classmethod
    def teardown_class(cls):
        cls.ds.delete()
