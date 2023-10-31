# Testing

In the repo there are 2 type of tests: unit tests and acceptance tests

## Unit tests

They live in the folder `tests/unit/` and the folder structure resembles the
file names. These tests are granular and don't have external requirements (they
don't use the API). That makes them very fast.

To run them:

```bash
RP_API_KEY="" pytest ravenpackapi/tests/unit
```

Note that we are _unsetting_ the API KEY just in case, since the tests don't
really need it. This is optional.

## Acceptance tests

THey are in the folder `tests/acceptance/` and they don't follow any particular
folder structure or naming convention. They are used to validate the library by
running multiple queries against the real API, so you need a valid API_KEY to
run them:

```bash
RP_API_KEY="XXXX" pytest ravenpackapi/tests/acceptance
```

Note that these tests are much slower and could fail easier, as they depend on
network connection and on RavenPack data.
