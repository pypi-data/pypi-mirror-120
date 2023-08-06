[![pypi](https://img.shields.io/pypi/v/tom-superevents.svg)](https://pypi.python.org/pypi/tom-superevents)
[![run-tests](https://github.com/TOMToolkit/tom_superevents/actions/workflows/run-tests.yml/badge.svg)](https://github.com/TOMToolkit/tom_superevents/actions/workflows/run-tests.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cbcf7ce565d8450f86fff863ef061ff9)](https://www.codacy.com/gh/TOMToolkit/tom_superevents/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=TOMToolkit/tom_superevents&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/TOMToolkit/tom_superevents/badge.svg?branch=main)](https://coveralls.io/github/TOMToolkit/tom_superevents?branch=main)

# GW Superevent (or GRB, Neutrino) EM follow-up

This reusable TOM Toolkit app provides support for gravitational wave (GW)
superevent electromagnetic (EM) follow up observations.  

## Installation

1. Install the package into your TOM environment:
    ```bash
    pip install tom_superevents
   ```

2. In your project `settings.py`, add `tom_superevents` to your `INSTALLED_APPS` setting:

    ```python
    INSTALLED_APPS = [
        ...
        'tom_superevents',
    ]
    ```

3. Include the tom_superevent URLconf in your project `urls.py`:
   ```python
   urlpatterns = [
        ...
        path('superevents/', include('tom_superevents.urls')),
   ]
   ```

4. Copy ``tom_superevents/templates/tom_common/base.html`` into your project root's ``templates/tom_common/base.html``.

5. Run ``python manage.py migrate`` to create the tom_superevent models.


## Running the tests

In order to run the tests, run the following in your virtualenv:

`python tom_superevent/tests/run_tests.py`

