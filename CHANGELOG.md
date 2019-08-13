# Changelog

## v1.0.32 (2019-08-13)
The RPApi instance gets two new methods:

* `get_document_url` to retrieve the document url from a RP_STORY_ID
* `get_flatfile_list` to retrieve the list of the available flatfiles for `companies`
 or `full` (for all the entities)

## v1.0.29 (2019-05-21)
**dataset creation explicit parameters**

The Dataset parameters are not explictly passed in the constructor
instead of being hidden in the kwargs.

This allows also to clearly support custom_fields and conditions.

A few new examples have been added or updated:
[get historical flat files](ravenpackapi/examples/get_historical_flat_files.py) and
[create a dataset with custom_fields and conditions](ravenpackapi/examples/indicator_datasets.py).

## v1.0.28 (2019-05-15)
**dataset.count method**

```python
dataset = api.get_dataset('us30')
data_count = ds.count(
    start_date='2018-01-05 18:00:00',
    end_date='2018-01-05 18:01:00',
)
# {'count': 11, 'stories': 10, 'entities': 6}

``` 
