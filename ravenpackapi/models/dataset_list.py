import logging

from ravenpackapi import Dataset

logger = logging.getLogger(__name__)


class DatasetList(object):
    def __init__(self, iterable):
        super(DatasetList, self).__init__()
        self.list = [dataset for dataset in iterable]

    @property
    def by_id(self):
        return {dataset.id: dataset for dataset in self.list}

    @property
    def by_name(self):
        """ Warning, the name is not guaranteed to be unique
        """
        result = {}
        for dataset in self.list:
            name = dataset.name
            if name in result:
                logger.warning("Multiple datasets with the same name: %s" % name)
            result[name] = dataset
        return result

    def __repr__(self):
        return "%d datasets" % len(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def __iter__(self):
        return self.list.__iter__()

    def __nonzero__(self):
        return bool(self.list)

    def __len__(self):
        return len(self.list)

    def __contains__(self, item):
        if isinstance(item, Dataset):
            dataset_id = item.uuid
            return dataset_id in self
        else:
            return item in self.by_id
