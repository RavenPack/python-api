import logging

import pytest

from ravenpackapi import RPApi, Dataset
from ravenpackapi.utils.helpers import delete_all_datasets_by_name

logger = logging.getLogger(__name__)


@pytest.mark.datasets
class TestDatasetCRUD(object):
    """ try to Create a dataset, Read it Update it and Delete it"""
    api = RPApi()
    dataset_name = 'testing_api_crud'

    def test_get_public_dataset_list(self):
        datasets = self.api.list_datasets(scope='public')
        assert 'us30' in datasets, 'US30 should be in public datasets'
        assert len(datasets) > 100, 'We expect at least 100 public RavenPack datasets'

    def test_get_private_dataset_list(self):
        datasets = self.api.list_datasets()
        assert len(datasets) > 0, "Don't you have a dataset?"

    def test_create_and_delete(self):
        # the test dataset is already there, let's delete it first
        # we can have multiple dataset with same name, deleting all of them
        delete_all_datasets_by_name(self.api, self.dataset_name)

        # create the dataset
        filters = {"rp_entity_id": {"$in": ['D8442A']}}
        dataset = Dataset(
            name=self.dataset_name,
            filters=filters,  # a dataset with a filter
        )
        new_dataset = self.api.create_dataset(
            dataset
        )
        assert new_dataset.filters == dataset.filters, "Created dataset filters are not as expected"
        assert new_dataset.id is not None, "We should have a dataset id"

        owned_dataset = self.api.list_datasets()
        assert new_dataset.id in owned_dataset, "We should own the new dataset"

        new_dataset.delete()

        owned_dataset = self.api.list_datasets()
        assert new_dataset.id not in owned_dataset, "The new dataset should be deleted"


class TestDatasetCreation(object):

    def test_valid_additional_fields(self):
        dt = '2020-01-01'
        d = Dataset(id='us30', creation_time=dt, last_modified=dt)
        assert d.id == 'us30'
        assert d.creation_time == d.last_modified == dt

    def test_valid_uuid(self):
        d = Dataset(uuid='us30')
        assert d.id == 'us30'

    def test_invalid_additional_fields(self):
        dt = '2020-01-01'
        with pytest.raises(ValueError):
            Dataset(id='us30', creation_time=dt, last_modified=dt, invalid_field=1)
