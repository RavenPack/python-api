RavenPack API - Python client
=============================

A Python library to consume the `RavenPack
API <https://www.ravenpack.com>`__.

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

Note
^^^^

This is still a work in progress. The API is stable and we are
continuing to update this Python wrapper.

Usage
-----

First, you'll need an API object that will deal with the API calls.

You will need a RavenPack API KEY, you can set the ``RP_API_KEY``
environment variable or set it in your code:

.. code:: python

    from ravenpackapi import RPApi

    api = RPApi(api_key="YOUR_API_KEY")

Getting data from the datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are several models to deal with data, the datasets are a cut of
the RavenPack data they are defined with a set of filters and a set of
fields.

.. code:: python

    # Get the dataset description from the server, here we use 'us30'
    # one of RavenPack public datasets with the top30 companies in the US  

    ds = api.get_dataset(dataset_id='us30')

Downloads: json
^^^^^^^^^^^^^^^

.. code:: python

    data = ds.json(
        start_date='2018-01-05 18:00:00',
        end_date='2018-01-05 18:01:00',
    )

    for record in data:
        print(record)

The json endpoint is handy for asking data synchronously, if you need to
download big data chunks you may want to use the asynchronous datafile
endpoint instead.

Json queries are limited to \* granular datasets: 10,000 records \*
indicator datasets: 500 entities, timerange 1Y, lookback 1Y

Downloads: datafile
^^^^^^^^^^^^^^^^^^^

For bigger requests the datafile endpoint can be used.

Requesting a datafile, will give you back a job promise, that will take
some time to complete.

.. code:: python

    job = ds.request_datafile(
        start_date='2018-01-05 18:00:00',
        end_date='2018-01-05 18:01:00',
    )

    with open('output.csv') as fp:
        job.save_to_file(filename=fp.name)

Realtime news-feed
~~~~~~~~~~~~~~~~~~

When you have a dataset you can subscribe to its realtime news-feed

.. code:: python

    ds = api.get_dataset(dataset_id='us500')
    for record in ds.request_realtime():
        print(record)
        print(record.timestamp_utc, record.entity_name,
                  record['event_relevance'])

The returned record takes care of converting the various fields to the
appropriate type, so ``record.timestamp_utc`` will be a ``datetime``

Entity reference
~~~~~~~~~~~~~~~~

The entity reference endpoint give you all the available information
over an Entity starting from the RP\_ENTITY\_ID

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
