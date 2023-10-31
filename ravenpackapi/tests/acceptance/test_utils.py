from ravenpackapi import Dataset, RPApi
from ravenpackapi.utils.helpers import delete_all_datasets_by_name, get_datasets_by_name


class TestDeleteAllByName(object):
    api = RPApi()
    base_dataset = Dataset(
        name="testing_api_delete_all",
        filters={},  # a dataset without filters
    )

    def test_delete_all_by_name(self):
        dataset_name = self.base_dataset.name

        delete_all_datasets_by_name(self.api, dataset_name)
        assert (
            len(get_datasets_by_name(self.api, dataset_name)) == 0
        ), "Seems we have datasets that should be deleted"

        ds1 = self.api.create_dataset(self.base_dataset)  # create 1...
        ds2 = self.api.create_dataset(self.base_dataset)  # create 2...

        assert (
            len(get_datasets_by_name(self.api, dataset_name)) == 2
        ), "We should have just created 2 datasets"

        # we can also check the new ones are in the owned
        owned_dataset = self.api.list_datasets()
        assert ds1 in owned_dataset
        assert ds2 in owned_dataset

        delete_all_datasets_by_name(self.api, dataset_name)
        assert (
            len(get_datasets_by_name(self.api, dataset_name)) == 0
        ), "Seems we have datasets that should be deleted"
