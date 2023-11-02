import uuid

import pytest

from ravenpackapi.models.dataset import Dataset


class TestDataset:
    def test_create_rpa_dataset(self, fake_api):
        dataset = Dataset(api=fake_api, name="test")
        assert dataset.name == "test"
        assert dataset.api == fake_api
        assert dataset.product == "RPA"
        dataset.save()
        assert fake_api.datasets["1"] == {
            "uuid": "1",
            "product": "RPA",
            "product_version": "1.0",
            "name": "test",
        }

    def test_create_edge_dataset(self, fake_api):
        dataset = Dataset(product="edge", api=fake_api, name="test")
        assert dataset.name == "test"
        assert dataset.api == fake_api
        assert dataset.product == "edge"
        dataset.save()
        fake_api.datasets["123"] = {
            "uuid": "123",
            "product": "edge",
            "product_version": "1.0",
            "name": "test",
        }

    def test_create_dataset_with_default_product(self, fake_api):
        dataset = Dataset(api=fake_api, name="test")
        assert dataset.product == "RPA"
        dataset.save()
        assert fake_api.datasets["1"] == {
            "uuid": "1",
            "product": "RPA",
            "product_version": "1.0",
            "name": "test",
        }

    def test_modify_existing_dataset(self, fake_api):
        # Given an edge dataset
        fake_api.datasets["123"] = {
            "uuid": "123",
            "product": "edge",
            "product_version": "1.0",
            "name": "test",
        }
        dataset = Dataset(uuid="123", api=fake_api)
        # When the lazy loading hasn't been triggered yet, the product is RPA
        assert dataset.product == "RPA"
        # When the dataset is modified, the lazy loading is triggered
        dataset.filters = {"$and": [{"rp_entity_id": {"$eq": "D8442A"}}]}
        # Then the product should be edge
        assert dataset.product == "edge"
        dataset.save()
        assert dataset.product == "edge"
        assert fake_api.datasets["123"] == {
            "uuid": "123",
            "product": "edge",
            "product_version": "1.0",
            "name": "test",
            "filters": {"$and": [{"rp_entity_id": {"$eq": "D8442A"}}]},
        }

    @pytest.fixture
    def fake_api(self):
        return FakeAPI()


class FakeAPI:
    def __init__(self):
        self.datasets = {}

    def request(self, endpoint, method="get", json=None):
        if method == "post":
            return self.post(endpoint, json)
        elif method == "put":
            return self.put(endpoint, json)
        elif method == "get":
            return self.get(endpoint)
        elif method == "delete":
            return self.delete(endpoint)
        else:
            raise NotImplementedError()

    def get(self, endpoint):
        if endpoint == "/datasets":
            # Actually this is not implemented in the Dataset class
            raise NotImplementedError(endpoint)
            # return FakeResponse({
            #     "datasets": [dataset for dataset in self.datasets.values()]
            # }, 200)
        if endpoint.startswith("/datasets/"):
            dataset_id = endpoint.split("/")[2]
            return FakeResponse(self.datasets[dataset_id].copy(), 200)
        raise NotImplementedError(endpoint)

    def post(self, endpoint, json):
        if endpoint == "/datasets":
            dataset_id = str(len(self.datasets) + 1)
            data = json.copy()
            data["uuid"] = dataset_id
            self.datasets[dataset_id] = data
            return FakeResponse({"dataset_uuid": dataset_id}, 200)
        elif endpoint.startswith("/datasets/"):
            dataset_id = endpoint.split("/")[2]
            self.datasets[dataset_id] = json.copy()
            return FakeResponse({"dataset_uuid": dataset_id}, 200)
        else:
            raise NotImplementedError(endpoint)

    def put(self, endpoint, json):
        if endpoint.startswith("/datasets/"):
            # This endpoint merges the existing dataset with the new data
            dataset_id = endpoint.split("/")[2]
            self.datasets[dataset_id].update(json)
            return FakeResponse({"dataset_uuid": dataset_id}, 200)
        else:
            raise NotImplementedError(endpoint)

    def delete(self, endpoint):
        raise NotImplementedError(endpoint)


class FakeResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data
