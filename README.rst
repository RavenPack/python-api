RavenPack API - Python client
=============================

A Python library to consume the
`RavenPack <https://www.ravenpack.com>`__ API.

`API documention. <https://www.ravenpack.com/support/>`__

Installation
------------

::

    pip install ravenpackapi

About
-----

The Python client helps managing the API calls to the RavenPack dataset
server in a Pythonic way, here are some examples of usage, you can find
more in the tests.

Usage
-----

In order to be able to use the RavenPack API you will need an API KEY.
If you don't already have one please contact your `customer
support <mailto:sales@ravenpack.com>`__ representative.

To begin using the API you will need to instantiate an API object that
will deal with the API calls.

Using your RavenPack API KEY, you can either set the ``RP_API_KEY``
environment variable or set it in your code:

.. code:: python

    from ravenpackapi import RPApi

    api = RPApi(api_key="YOUR_API_KEY")

Getting data from the datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the API wrapper, there are several models that maybe used for
interacting with data.

Here is how you may get a dataset definition for a pre-existing dataset

.. code:: python

    # Get the dataset description from the server, here we use 'us30'
    # one of RavenPack public datasets with the top30 companies in the US  

    ds = api.get_dataset(dataset_id='us30')

Downloads: json
^^^^^^^^^^^^^^^

The json endpoint is useful for asking data synchronously, optimized for
small requests, if you need to download big data chunks you may want to
use the asynchronous datafile endpoint instead.

.. code:: python

    data = ds.json(
        start_date='2018-01-05 18:00:00',
        end_date='2018-01-05 18:01:00',
    )

    for record in data:
        print(record)

Json queries are limited to \* granular datasets: 10,000 records \*
indicator datasets: 500 entities, timerange 1 year, lookback window 1
year

Downloads: datafile
^^^^^^^^^^^^^^^^^^^

For bigger requests the datafile endpoint can be used to prepare a
datafile asynchronously on the RavenPack server for later retrieval.

Requesting a datafile, will give you back a job object, that will take
some time to complete.

.. code:: python

    job = ds.request_datafile(
        start_date='2018-01-05 18:00:00',
        end_date='2018-01-05 18:01:00',
    )

    with open('output.csv') as fp:
        job.save_to_file(filename=fp.name)

Streaming real-time data
~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to subscribe to a real-time stream for a dataset:

.. code:: python

    ds = api.get_dataset(dataset_id='us500')
    for record in ds.request_realtime():
        print(record)
        print(record.timestamp_utc, record.entity_name,
                  record['event_relevance'])

The Result object takes care of converting the various fields to the
appropriate type, so ``record.timestamp_utc`` will be a ``datetime``

Entity reference
~~~~~~~~~~~~~~~~

The entity reference endpoint give you all the available information for
an Entity given the RP\_ENTITY\_ID

.. code:: python

    ALPHABET_RP_ENTITY_ID = '4A6F00'

    references = api.get_entity_reference(ALPHABET_RP_ENTITY_ID)

    # show all the names over history
    for name in references.names:
        print(name.value, name.start, name.end)
        
    # print all the ticket valid today
    for ticker in references.tickers:
        if ticker.is_valid():
            print(ticker)
