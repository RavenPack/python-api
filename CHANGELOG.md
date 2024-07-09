# Changelog

## [Unreleased]

## [v1.1.5] (2024-06-28)

### Changed

- Removed the dependency on the library `retry` (and the indirect dependency on
  `py`), and replaced it with `tenacity`. This should be transparent.

## [v1.1.4] (2024-02-01)

### Fixed

Fixed issue creating an Edge dataset without product attribute specified, but specifying the product in the `RPApi` object:

```python
from ravenpackapi import RPApi, Dataset

api = RPApi(api_key="YOUR_API_KEY", product="edge")

ds = api.create_dataset(
    Dataset(
        name="New Dataset",
        filters={"entity_relevance": {"$gte": 90}},
    )
)
```

Since the product is not specified in `Dataset`'s `__init__`, the incorrect
product was being passed to the API, resulting in the message.

> Field 'product' must be 'edge'

## [v1.1.3] (2023-12-06)

### Fixed

- Fixed corner case when the entity-mapping doesn't return any entity but also
  there are no errors

### Changed

- Default timeout for request increased from 60 seconds to 100 seconds to match
  the timeout in the API. The default connection timeout is still 10 seconds.

### Added

- Added some examples.

## [v1.1.2] (2023-10-03)

### Fixed

Fixed a bug in setup.py that caused a crash when running

```
python setup.py egg_info
```

## [v1.1.1] (2023-10-02)

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

## [v1.1.0] (2023-09-21)

### Added

- Support for anaconda
- New Github Actions pipeline

## [v1.0.60] (2023-09-13)

### Added
New flag to store the entity mapping data in memory, when using `edge`. Use
with caution.

```python
eref = api.get_entity_type_reference(entity_type, "full", file_date)
eref.store_in_memory = True
for entity in eref:
    print(entity)
```

## [v1.0.59] (2022-11-25)

### Added

- New examples

### Improved
- Script to check the connection (check_connection.py) also checks edge.
- Edge flatfiles can now be downloaded through the API, just like RPA
  flatfiles
- Old examples now work with edge as well. 

### Fixed

- Bug listing jobs

## [v1.0.58] (2022-01-12)

### Improved

`EntityTypeReference` for Edge reference files won't keep the entire mapping in
memory anymore. This allows to grab the reference files and write them to file
(or iterate through them) but they can't be accessed as rp_entity_id mappings
anymore. For Edge only.

## [v1.0.57] (2021-11-24)

### Fixed

- Bug in event_symilarity_days serializer
- Bug with UTF-8 encoding in the edge reference-type

## [v1.0.56] (2021-11-04)

### Improved

Internal changes to speed up `get_status` and `wait_for_completion` file methods

## [v1.0.55] (2021-10-15)

### Added

Added an optional parameter `upload_mode` to `api.upload.file`, which can be
"RPXML" or "RPJSON". Internal.

## [v1.0.54] (2021-10-14)

### Fixed

Fix for `Result`.__str__ to handle Edge fields

### Changed

Datafile's content now don't contain empty records

## [v1.0.53] (2021-08-26)

### Added

Product aware instance: allows to access edge just instanciating your api with

```python
api = RPApi(product="edge")
```

## [v1.0.52] (2021-08-20)

### Added

Entity-type-reference: support to retrieve a reference in the past. It also
supports to specify `reference_type="delta"` to retrieve just a daily
difference of the changes (only for Edge).

## [v1.0.51] (2021-08-11)

### Added
Insider-transactions and Earnings-Dates API support: list the available files
and download them to automate your process

## [v1.0.50] (2021-07-20)

### Fixed

Fix for Python 2.7 compatibility

## [v1.0.49] (2021-07-16)

### Added

Text analytics: support for uploading via source_url

## [v1.0.48] (2021-07-10)

### Added

Text analytics: support for the /text-extraction endpoint

## [v1.0.47] (2021-04-12)

### Added

Text analytics: Handle retry if too early on /metadata endpoint

## [v1.0.46] (2021-04-05)

### Added

Compatibility with RavenPack Edge

* loosen validation for entity-types (in Edge we have various dynamical EDETs)
* loosen validation for RT fields (in Edge we have several new fields)

## [v1.0.45] (2021-01-30)

### Added

* Support for `PRDT` (product-type) in the entity_reference endpoint
* Retry logic on 425 status code in some text-analytics API calls

## [v1.0.44] (2020-12-09)

### Added

* Retry logic on 404 status code in some text-analytics API calls
* Added entity type to the EntityTypeReference object
* Improved validation of invalid fields when initializing the dataset

## [v1.0.43] (2020-11-04)

### Added

* Entity-mapping - expose the matching score and the candidates

## [v1.0.42] (2020-10-19)

### Fixed

* Bug in pagination of files endpoint

## [v1.0.41] (2020-10-08)

### Improved

`get_status` on an uploaded file now refreshes all of the metadata, not just
the status.

## [v1.0.40] -YANKED- (2020-10-07)

### Added

* Support for the /jobs endpoint (to list the user past endpoints)

**NOTE*** This version is not available in PyPI

## [v1.0.39] (2020-09-22)

### Improved

* Persistent sessions between API-calls

## [v1.0.38] (2020-09-04)

### Added

* Text-Analytics API additional functions: `get_analytics` and `get_annotated`

## [v1.0.37] (2020-06-16)

### Added

* Creating and saving folders in Text-Analytics
* New `save` method on `File`

### Changed

* Renamed filter `filename` parameter to `file_name` in `UploadApi.list()`
* Entity reference is now sorted by `range_start`

### Fixed

* Better error catching for realtime feed subscriptions

## [v1.0.36] (2020-05-14)

### Changed

* Text-Analytics API endpoint updated: folders & richer metadata
* Extended error handling to support Feed disconnection problems

## [v1.0.35] (2020-02-22)

### Added

Initial support for the Text-Analytics API endpoints

## [v1.0.34] (2019-11-11)

### Added

Retrieve a lazy-loaded dataset when setting one of its paramters.

## [v1.0.33] (2019-10-17)

### Changed

* A default timeout of 10" on connection and 60" on silence has been added to all the API calls
* Retrieve or save a flatfile using the new methods `get_flatfile` and `save_flatfile`.
  See `get_historical_flat_list.py` for a complete example.

## [v1.0.32] (2019-08-13)

### Added

The RPApi instance gets two new methods:

* `get_document_url` to retrieve the document url from a RP_STORY_ID
* `get_flatfile_list` to retrieve the list of the available flatfiles for `companies`
  or `full` (for all the entities)

## [v1.0.31] (2019-07-14)

### Added

* Ad-hoc `api.json()` method now supports `conditions` and `custom_fields`

## [v1.0.30] (2019-06-11)

### Added

* New parameter `common_request_params` added to the RT stream requests.

## [v1.0.29] (2019-05-21)

### Changed

**dataset creation explicit parameters**

The Dataset parameters are not explictly passed in the constructor instead of
being hidden in the kwargs.

This allows also to clearly support custom_fields and conditions.

A few new examples have been added or updated:
[get historical flat files](ravenpackapi/examples/get_historical_flat_files.py) and
[create a dataset with custom_fields and conditions](ravenpackapi/examples/indicator_datasets.py).

## [v1.0.28] (2019-05-15)

### Added

New `dataset.count` method

```python
dataset = api.get_dataset('us30')
data_count = ds.count(
    start_date='2018-01-05 18:00:00',
    end_date='2018-01-05 18:01:00',
)
# {'count': 11, 'stories': 10, 'entities': 6}
```

## [v1.0.27] (2019-05-03)

### Added

* New `ApiConnectionError`
* `request_realtime` method now supports `keep_alive`

## [v1.0.26] (2019-04-23)

### Added

New `common_request_params` attribute on the `RPApi` object to send extra
params to the requests library

## [v1.0.25] (2019-03-12)

### Improved

`request_realtime` now doesn't buffer RT requests to avoid waiting for chunks.

## [v1.0.24] (2018-20-11)

### Added

Support for the job cancellation endpoint (while a job is in the ENQUEUED
state)

```python
job = ds.request_datafile(...)
job.cancel()
```

### Improved

`Job.wait_for_completion` raises an exception if the job goes in `ERROR` so we
don't wait forever.

## [v1.0.23] (2018-09-20)

### Fixed

Fixed encoding issues with differences in Python2 and Python3

### Improved

Jobs are now iterable

## [v1.0.22] (2018-09-12)

### Added

Created `EntityTypeReference` to query the whole of entity reference

## [v1.0.21] (2018-07-24)

### Changed

Requesting Ad-Hoc `json()` will use the dataset frequency as the default one

## [v1.0.20] (2018-07-19)

### Changed

Saving job to file raises an exception when there is an error in the API call

## [v1.0.19] (2018-05-03)

### Added

Added 2 more options (`SPLIT_WEEKLY` and `SPLIT_DAILY`) to the method `time_intervals`, used to download a datafile in chunks:

```python
from ravenpackapi.util import (
  SPLIT_YEARLY,
  SPLIT_MONTHLY,
  SPLIT_WEEKLY,
  SPLIT_DAILY,
  time_intervals
)
split = SPLIT_DAILY
for range_start, range_end in time_intervals(start_date, end_date, split=split):
    job = ds.request_datafile(
        start_date=range_start,
        end_date=range_end,
        compressed=GET_COMPRESSED,
    )
    ...
```

## [v1.0.18] (2018-04-17)

### Added

Now datasets can not only be created but updated as well via the
`dataset.save()` method.

## [v1.0.17] (2018-03-29)

### Fix

Hotfix for missing module in package.

## [v1.0.16] (2018-03-29)

### Fixed

Hotfix for missing module in package.


## [v1.0.15] (2018-03-13)

### Added

New `get_entity_mapping` method to retrieve the entity mapping

### Fixed

Fix bug with encoding in Python2

## [v1.0.14] (2018-03-09)


### Added

Timezone support for datafiles

```python
custom_dataset = Dataset(
    api=api,
    name="Us30 indicators",
    filters=us30.filters,
    fields=new_fields,
    frequency='daily'
)
custom_dataset.save()
print(custom_dataset)
job = custom_dataset.request_datafile(
    start_date='2017-01-01 19:30',
    end_date='2017-01-02 19:30',
    compressed=True,
    time_zone='Europe/London',
)
```

## [v1.0.13] (2018-03-08)

### Improved

Better error handling requesting datafiles via `ds.request_datafile()`

## [v1.0.12] (2018-03-08)
## [v1.0.11] (2018-03-08)

### Changed

* Requesting a datafile now raises an `APIException` when the API returns a
  `400` code.
* Date params on the datafile request can be now both strings and datetime
  objects.

### Added

Added helper method `time_intervals` to split the datafile requests in smaller
intervals.


## [v1.0.10] (2018-03-06)

### Changed

`iterate_results()` method now returns rows as a list of strings, rather than a
single string.


## [v1.0.9] (2018-03-06)

### Added

* New `Dataset.save()` method to create new datasets.
* New `Job.iterate_results()` method to iterate over the rows of the results
  without saving the file.

## [v1.0.8] (2018-03-06)

### Fixed

Fixed missing dependencies

## [v1.0.7] (2018-03-05)

### Added

New `Dataset.request_realtime` method to request data in real-time.
New `Result` object to map analytic fields

## [v1.0.6] (2018-03-02)

### Added

Allow dataset requests to be tagged


## [v1.0.5] (2018-03-02)
## [v1.0.4] (2018-03-02)
## [v1.0.3] (2018-02-20)

### Added

New methods in `RPEntityMetadata`

## [v1.0.2] (2018-01-30)

### Added

Getting entity reference through `get_entity_reference`.

## [v1.0.1] (2018-01-30)

### Added

* New methods in `RPApi`
    * `api.get_dataset()` to retrieve an existing dataset from the API
    * `api.json()` to make an _ad-hoc_ request
* New methods in the `Dataset` class
    * `Dataset.delete()`
    * `Dataset.json()`
    * `Dataset.request_datafile()`
* New `DatasetList` class to list all the datasets in the account
* More attributes and methods on the Job object
    * `get_status()`
    * `wait_for_completion()`
    * `save_to_file()`

## [v1.0.0] (2018-01-26)

First _non-beta_ release

[Unreleased]: https://github.com/RavenPack/python-api/compare/v1.1.5...HEAD
[v1.1.5]: https://github.com/RavenPack/python-api/compare/v1.1.4...v1.1.5
[v1.1.4]: https://github.com/RavenPack/python-api/compare/v1.1.3...v1.1.4
[v1.1.3]: https://github.com/RavenPack/python-api/compare/v1.1.2...v1.1.3
[v1.1.2]: https://github.com/RavenPack/python-api/compare/v1.1.1...v1.1.2
[v1.1.1]: https://github.com/RavenPack/python-api/compare/v1.1.0...v1.1.1
[v1.1.0]: https://github.com/RavenPack/python-api/compare/v1.0.60...v1.1.0
[v1.0.60]: https://github.com/RavenPack/python-api/compare/v1.0.59...v1.0.60
[v1.0.59]: https://github.com/RavenPack/python-api/compare/v1.0.58...v1.0.59
[v1.0.58]: https://github.com/RavenPack/python-api/compare/v1.0.57...v1.0.58
[v1.0.57]: https://github.com/RavenPack/python-api/compare/v1.0.56...v1.0.57
[v1.0.56]: https://github.com/RavenPack/python-api/compare/v1.0.55...v1.0.56
[v1.0.55]: https://github.com/RavenPack/python-api/compare/v1.0.54...v1.0.55
[v1.0.54]: https://github.com/RavenPack/python-api/compare/v1.0.53...v1.0.54
[v1.0.53]: https://github.com/RavenPack/python-api/compare/v1.0.52...v1.0.53
[v1.0.52]: https://github.com/RavenPack/python-api/compare/v1.0.51...v1.0.52
[v1.0.51]: https://github.com/RavenPack/python-api/compare/v1.0.50...v1.0.51
[v1.0.50]: https://github.com/RavenPack/python-api/compare/v1.0.49...v1.0.50
[v1.0.49]: https://github.com/RavenPack/python-api/compare/v1.0.48...v1.0.49
[v1.0.48]: https://github.com/RavenPack/python-api/compare/v1.0.47...v1.0.48
[v1.0.47]: https://github.com/RavenPack/python-api/compare/v1.0.46...v1.0.47
[v1.0.46]: https://github.com/RavenPack/python-api/compare/v1.0.45...v1.0.46
[v1.0.45]: https://github.com/RavenPack/python-api/compare/v1.0.44...v1.0.45
[v1.0.44]: https://github.com/RavenPack/python-api/compare/v1.0.43...v1.0.44
[v1.0.43]: https://github.com/RavenPack/python-api/compare/v1.0.42...v1.0.43
[v1.0.42]: https://github.com/RavenPack/python-api/compare/v1.0.41...v1.0.42
[v1.0.41]: https://github.com/RavenPack/python-api/compare/v1.0.40...v1.0.41
[v1.0.40]: https://github.com/RavenPack/python-api/compare/v1.0.39...v1.0.40
[v1.0.39]: https://github.com/RavenPack/python-api/compare/v1.0.38...v1.0.39
[v1.0.38]: https://github.com/RavenPack/python-api/compare/v1.0.37...v1.0.38
[v1.0.37]: https://github.com/RavenPack/python-api/compare/v1.0.36...v1.0.37
[v1.0.36]: https://github.com/RavenPack/python-api/compare/v1.0.35...v1.0.36
[v1.0.35]: https://github.com/RavenPack/python-api/compare/v1.0.34...v1.0.35
[v1.0.34]: https://github.com/RavenPack/python-api/compare/v1.0.33...v1.0.34
[v1.0.33]: https://github.com/RavenPack/python-api/compare/v1.0.32...v1.0.33
[v1.0.32]: https://github.com/RavenPack/python-api/compare/v1.0.31...v1.0.32
[v1.0.31]: https://github.com/RavenPack/python-api/compare/v1.0.30...v1.0.31
[v1.0.30]: https://github.com/RavenPack/python-api/compare/v1.0.29...v1.0.30
[v1.0.29]: https://github.com/RavenPack/python-api/compare/v1.0.28...v1.0.29
[v1.0.28]: https://github.com/RavenPack/python-api/compare/v1.0.27...v1.0.28
[v1.0.27]: https://github.com/RavenPack/python-api/compare/v1.0.26...v1.0.27
[v1.0.26]: https://github.com/RavenPack/python-api/compare/v1.0.25...v1.0.26
[v1.0.25]: https://github.com/RavenPack/python-api/compare/v1.0.24...v1.0.25
[v1.0.24]: https://github.com/RavenPack/python-api/compare/v1.0.23...v1.0.24
[v1.0.23]: https://github.com/RavenPack/python-api/compare/v1.0.22...v1.0.23
[v1.0.22]: https://github.com/RavenPack/python-api/compare/v1.0.21...v1.0.22
[v1.0.21]: https://github.com/RavenPack/python-api/compare/v1.0.20...v1.0.21
[v1.0.20]: https://github.com/RavenPack/python-api/compare/v1.0.19...v1.0.20
[v1.0.19]: https://github.com/RavenPack/python-api/compare/v1.0.18...v1.0.19
[v1.0.18]: https://github.com/RavenPack/python-api/compare/v1.0.17...v1.0.18
[v1.0.17]: https://github.com/RavenPack/python-api/compare/v1.0.16...v1.0.17
[v1.0.16]: https://github.com/RavenPack/python-api/compare/v1.0.15...v1.0.16
[v1.0.15]: https://github.com/RavenPack/python-api/compare/v1.0.14...v1.0.15
[v1.0.14]: https://github.com/RavenPack/python-api/compare/v1.0.13...v1.0.14
[v1.0.13]: https://github.com/RavenPack/python-api/compare/v1.0.12...v1.0.13
[v1.0.12]: https://github.com/RavenPack/python-api/compare/v1.0.11...v1.0.12
[v1.0.11]: https://github.com/RavenPack/python-api/compare/v1.0.10...v1.0.11
[v1.0.10]: https://github.com/RavenPack/python-api/compare/v1.0.9...v1.0.10
[v1.0.9]: https://github.com/RavenPack/python-api/compare/v1.0.8...v1.0.9
[v1.0.8]: https://github.com/RavenPack/python-api/compare/v1.0.7...v1.0.8
[v1.0.7]: https://github.com/RavenPack/python-api/compare/v1.0.6...v1.0.7
[v1.0.6]: https://github.com/RavenPack/python-api/compare/v1.0.5...v1.0.6
[v1.0.5]: https://github.com/RavenPack/python-api/compare/v1.0.4...v1.0.5
[v1.0.4]: https://github.com/RavenPack/python-api/compare/v1.0.3...v1.0.4
[v1.0.3]: https://github.com/RavenPack/python-api/compare/v1.0.2...v1.0.3
[v1.0.2]: https://github.com/RavenPack/python-api/compare/v1.0.1...v1.0.2
[v1.0.1]: https://github.com/RavenPack/python-api/compare/v1.0.0...v1.0.1
[v1.0.0]: https://github.com/RavenPack/python-api/releases/tag/v1.0.0
