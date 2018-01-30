import logging

logger = logging.getLogger(__name__)


def delete_all_datasets_by_name(api, dataset_name):
    to_be_deleted = get_datasets_by_name(api, dataset_name)
    for dataset in to_be_deleted:
        logger.debug("Deleting the dataset {name} [{id}]".format(
            name=dataset_name, id=dataset.id
        ))
        dataset.delete()
    return len(to_be_deleted)


def get_datasets_by_name(api, dataset_name, scope='private'):
    datasets = api.list_datasets(scope=scope)
    return [d for d in datasets if d.name == dataset_name]
