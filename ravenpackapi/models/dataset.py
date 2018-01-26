class Dataset:
    READ_ONLY_FIELDS = {'creation_time', 'last_modified'}
    VALID_FIELDS = {'uuid', 'name', 'description',
                    'tags', 'product', 'product_version',
                    'frequency', 'fields', 'filters', } | READ_ONLY_FIELDS

    def __init__(self, **kwargs) -> None:
        super(Dataset, self).__init__()
        self._data = kwargs

    @staticmethod
    def from_dict(item):
        return Dataset(
            **{k: v for k, v in item.items() if k in Dataset.VALID_FIELDS}
        )

    # def __setattr__(self, key, value):
    #     if key == 'id':
    #         key = 'uuid'
    #     if key not in Dataset.VALID_FIELDS:
    #         raise ValueError("Invalid field %s" % key)
    #     if key == 'uuid':
    #         raise ValueError("You cannot set dataset UUID")

    @property
    def id(self):  # an alias for the dataset unique id
        return self.uuid

    def __getattr__(self, field):
        if field in Dataset.VALID_FIELDS:
            return self._data[field]
        else:
            return self.__getattribute__(field)

    def as_dict(self):
        valid_obj = {k: self._data[k]
                     for k in Dataset.VALID_FIELDS
                     if k in self._data}
        return valid_obj

    def __str__(self):
        return "Dataset: {name} [{id}]".format(
            name=self.name, id=self.id,
        )


class DatasetList:
    def __init__(self, iterable) -> None:
        super(DatasetList, self).__init__()
        self.list = [dataset for dataset in iterable]

    @property
    def by_id(self):
        return {dataset.id: dataset for dataset in self.list}

    def __str__(self):
        return "%d datasets" % len(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def __iter__(self):
        return self.list.__iter__()

    def __nonzero__(self):
        return bool(self.list)

    def __len__(self):
        return len(self.list)
