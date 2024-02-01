import pytest

from ravenpackapi.models.dataset import Dataset


class TestDataset:
    def test_create_rpa_dataset(self, fake_api):
        dataset = Dataset(product="rpa", api=fake_api, name="test")
        assert dataset.name == "test"
        assert dataset.api == fake_api
        assert dataset.product == "rpa"
        dataset.save()
        assert fake_api.datasets["1"] == {
            "uuid": "1",
            "product": "rpa",
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

    @pytest.mark.parametrize(
        "product",
        ["rpa", "edge"],
    )
    def test_create_dataset_with_default_product(self, product):
        fake_api = FakeAPI(product=product)
        dataset = Dataset(api=fake_api, name="test")
        assert dataset.product == product
        dataset.save()
        assert fake_api.datasets["1"] == {
            "uuid": "1",
            "product": product,
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
        assert dataset.product == "edge"
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

    def test_saving_a_dataset_without_changing_anything(
        self, valid_fields_with_specific_order
    ):
        _ = valid_fields_with_specific_order  # Ignore fixture not used warning
        # Given an edge dataset
        fake_api = FakeAPI()
        fake_api.datasets["123"] = {
            "uuid": "123",
            "product": "edge",
            "product_version": "1.0",
            "name": "test",
        }
        dataset = Dataset(uuid="123", api=fake_api)
        # When the lazy loading hasn't been triggered yet, the product is RPA
        assert dataset.product == "edge"
        dataset.save()
        assert dataset.product == "edge"
        assert fake_api.datasets["123"] == {
            "uuid": "123",
            "product": "edge",  # Test fails here because we are saving RPA
            "product_version": "1.0",
            "name": "test",
        }

    @pytest.fixture
    def valid_fields_with_specific_order(self):
        # Given a specific order of valid fields
        old_valid_fields = Dataset._VALID_FIELDS
        Dataset._VALID_FIELDS = [
            "product",
            "name",
            "description",
            "tags",
            "product_version",
            "frequency",
            "fields",
            "filters",
            "tags",
            "having",
            "custom_fields",
            "conditions",
        ] + list(Dataset._READ_ONLY_FIELDS)
        yield
        Dataset._VALID_FIELDS = old_valid_fields

    @pytest.fixture
    def fake_api(self):
        return FakeAPI()


class FakeAPI:
    def __init__(self, product="rpa"):
        self.datasets = {}
        self.product = product

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
