import pytest

from ravenpackapi import RPApi, Dataset


@pytest.mark.datasets
class TestDatasetList(object):
    api = RPApi()

    def test_list_public_filters(self):
        # we get name and id for dataset
        datasets = self.api.list_datasets(scope="public")

        # iterating it should automatically get the dataset to return the filters
        for ds in datasets[:3]:
            assert ds.id and ds.uuid and ds.name and ds.filters


@pytest.mark.datasets
class TestDatasetRetrieval(object):
    api = RPApi()

    def test_get_dataset(self):
        dataset_id = 'us30'
        ds_by_id = Dataset(api=self.api, id=dataset_id)
        filters = ds_by_id.filters

        assert isinstance(filters, dict)

        ds_via_api = self.api.get_dataset(dataset_id)
        ds_by_uuid = Dataset(api=self.api, uuid=dataset_id)

        assert ds_via_api.filters == ds_by_id.filters == ds_by_uuid.filters
