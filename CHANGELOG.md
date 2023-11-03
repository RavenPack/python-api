# Changelog

## v1.1.2 (2023-10-03)

### Fixed

Fixed a bug in setup.py that caused a crash when running

```
python setup.py egg_info
```

## v1.1.1 (2023-10-02)

### Removed

* Removed dependency on `future` #9

### Fixed

Fixed bug with lazy loading that caused the wrong product (`RPA`) being sent
_sometimes_ when saving a dataset without modifying it.

To reproduce the issue:
```python
from ravenpackapi import RPApi
api = RPApi(product="edge")
ds = api.get_dataset("SOME_DATASET_ID")
ds.save()
```

Note that this error is not always triggered and is not deterministic.

## v1.1.0 (2023-09-21)

### Added

- Support for anaconda
- New Github Actions pipeline

## v1.0.60 (2023-09-13)

### Added
New flag to store the entity mapping data in memory, when using `edge`. Use
with caution.

```python
eref = api.get_entity_type_reference(entity_type, "full", file_date)
eref.store_in_memory = True
for entity in eref:
    print(entity)
```

## v1.0.59 (2022-11-25)

### Added

- New examples

### Improved
- Script to check the connection (check_connection.py) also checks edge.
- Edge flatfiles can now be downloaded through the API, just like RPA
  flatfiles
- Old examples now work with edge as well. 

### Fixed

- Bug listing jobs

## v1.0.58 (2022-01-12)

### Improved
`EntityTypeReference` for Edge reference files won't keep the entire mapping in
memory anymore. This allows to grab the reference files and write them to file
(or iterate through them) but they can't be accessed as rp_entity_id mappings
anymore. For Edge only.

## v1.0.56 (2021-11-04)

Internal changes to speed up get_status and wait_for_completion file methods

## v1.0.53 (2021-08-26)

Product aware instance: allows to access edge just instanciating your api with

```python
api = RPApi(product="edge")
```

## v1.0.52 (2021-08-20)

Entity-type-reference: support to retrieve a reference in the past. It also supports to specify `reference_type="delta"`
to retrieve just a daily difference of the changes (only for Edge).

## v1.0.51 (2021-08-11)

Insider-transactions and Earnings-Dates API support:
list the available files and download them to automate your process

## v1.0.49 (2021-07-16)

Text analytics: support for uploading via source_url

## v1.0.48 (2021-07-10)

Text analytics: support for the /text-extraction endpoint

## v1.0.47 (2021-04-12)

Text analytics: Handle retry if too early on /metadata endpoint

## v1.0.46 (2021-04-05)

Compatibility with RavenPack Edge

* loosen validation for entity-types (in Edge we have various dynamical EDETs)

* loosen validation for RT fields (in Edge we have several new fields)

## v1.0.43 (2020-11-04)

* Entity-mapping - expose the matching score and the candidates

## v1.0.40 (2020-10-07)

* Support for the /jobs endpoint (to list the user past endpoints)

## v1.0.39 (2020-09-22)

* Persistent sessions between API-calls

## v1.0.38 (2020-09-04)

* Text-Analytics API additional functions: `get_analytics` and `get_annotated`

## v1.0.36 (2020-05-14)

* Text-Analytics API endpoint updated: folders & richer metadata
* Extended error handling to support Feed disconnection problems

## v1.0.35 (2020-02-22)

Initial support for the Text-Analytics API endpoints

## v1.0.34 (2019-11-11)

Retrieve a lazy-loaded dataset when setting one of its paramters.

## v1.0.33 (2019-10-17)

* A default timeout of 10" on connection and 60" on silence has been added to all the API calls
* Retrieve or save a flatfile using the new methods `get_flatfile` and `save_flatfile`.
  See `get_historical_flat_list.py` for a complete example.

## v1.0.32 (2019-08-13)

The RPApi instance gets two new methods:

* `get_document_url` to retrieve the document url from a RP_STORY_ID
* `get_flatfile_list` to retrieve the list of the available flatfiles for `companies`
  or `full` (for all the entities)

## v1.0.29 (2019-05-21)

**dataset creation explicit parameters**

The Dataset parameters are not explictly passed in the constructor instead of being hidden in the kwargs.

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
