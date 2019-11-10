import pytest

from ravenpackapi import RPApi, Dataset
from ravenpackapi.utils.helpers import delete_all_datasets_by_name


@pytest.mark.datasets
class TestDatasetUpdate(object):
    """ try to Create a dataset, Read it Update it and Delete it"""
    api = RPApi()
    dataset_name = 'testing_ds_update'

    def test_create_and_update(self):
        delete_all_datasets_by_name(self.api, self.dataset_name)
        filters = {"rp_entity_id": {"$in": ['AAAAAA']}}
        dataset = Dataset(
            name=self.dataset_name,
            filters=filters,  # a dataset with a filter
        )
        dataset = self.api.create_dataset(dataset)

        assert dataset.id is not None
        dataset_id = dataset.id

        # change the dataset
        new_filters = {"rp_entity_id": {"$in": ['BBBBBB']}}
        dataset.filters = new_filters
        dataset.save()

        # get the dataset again
        dataset = self.api.get_dataset(dataset_id)
        assert dataset.filters == new_filters
        new_filters = {"rp_entity_id": {"$in": ['CCCCCC']}}
        dataset.filters = new_filters
        dataset.save()

        dataset.delete()

        assert delete_all_datasets_by_name(self.api, self.dataset_name) == 0

    def test_simple_update(self):
        filters = {"rp_entity_id": {"$in": ['D8442A']}}
        ds = self.api.create_dataset(
            Dataset(
                name=self.dataset_name,
                filters=filters,  # a dataset with a filter
            )
        )
        assert ds._lazy_retrieve_on_get is False

        dataset_id = ds.id

        ds = self.api.get_dataset(dataset_id)  # retrieve the dataset
        assert ds._lazy_retrieve_on_get is True  # it still have to be lazy loaded here
        ds.filters = {"rp_entity_id": {"$in": ["228D42"]}}  # update the dataset ***
        ds.save()

        for r in ds.json('2019-01-01', '2019-01-02'):
            assert r['rp_entity_id'] == '228D42', "Expecting entity to be 228D42 - got %s" % r['rp_entity_id']
            break
