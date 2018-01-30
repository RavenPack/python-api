from ravenpackapi import RPApi, Dataset
from ravenpackapi.util import to_curl
from ravenpackapi.utils.helpers import delete_all_datasets_by_name, get_datasets_by_name


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class TestToCurl(object):
    def test_normal_curl(self):
        request = AttrDict(method='GET',
                           headers={'API-KEY': 'test'},
                           body=None,
                           url='http://test')
        assert to_curl(request) == 'curl -X GET -H \'API-KEY:test\' \'http://test\''

    def test_missing_request(self):
        request = None
        assert to_curl(request) == 'No request'


class TestDeleteAllByName(object):
    api = RPApi()
    base_dataset = Dataset(
        name='testing_api_delete_all',
        filters={},  # a dataset without filters
    )

    def test_delete_all_by_name(self):
        dataset_name = self.base_dataset.name

        delete_all_datasets_by_name(self.api, dataset_name)
        assert len(
            get_datasets_by_name(self.api, dataset_name)
        ) == 0, "Seems we have datasets that should be deleted"

        ds1 = self.api.create_dataset(self.base_dataset)  # create 1...
        ds2 = self.api.create_dataset(self.base_dataset)  # create 2...

        assert len(
            get_datasets_by_name(self.api, dataset_name)
        ) == 2, "We should have just created 2 datasets"

        # we can also check the new ones are in the owned
        owned_dataset = self.api.list_datasets()
        assert ds1 in owned_dataset
        assert ds2 in owned_dataset

        delete_all_datasets_by_name(self.api, dataset_name)
        assert len(
            get_datasets_by_name(self.api, dataset_name)
        ) == 0, "Seems we have datasets that should be deleted"
