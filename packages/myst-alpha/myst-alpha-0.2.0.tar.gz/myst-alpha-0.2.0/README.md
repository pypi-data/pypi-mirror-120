# Myst Python Library

This is the official Python client library for the Myst Platform.

## Requirements

- Python 3.7+

## Installation

To install the package from PyPI:

    $ pip install --upgrade myst-alpha

## Authentication

The Myst API uses JSON Web Tokens (JWTs) to authenticate requests.

The Myst Python library handles the sending of JWTs to the API automatically and currently supports two ways to authenticate to obtain a JWT: through your Google user account or a Myst service account.

### Authenticating using your user account

If you don't yet have a Google account, you can create one on the [Google Account Signup](https://accounts.google.com/signup) page.

Once you have access to a Google account, send an email to `support@myst.ai` with your email so we can authorize you to use the Myst Platform.

Use the following code snippet to authenticate using your user account:

```python
import myst

myst.authenticate()
```

The first time you run this, you'll be presented with a web browser and asked to authorize the Myst Python library to make requests on behalf of your Google user account.

### Authenticating using a service account

You can also authenticate using a Myst service account. To request a service account, email `support@myst.ai`.

To authenticate using a service account, set the `MYST_APPLICATION_CREDENTIALS` environment variable to the path to your service account key file:

```sh
$ export MYST_APPLICATION_CREDENTIALS=</path/to/key/file.json>
```

Then, go through the service account authentication flow:

```python
import myst

myst.authenticate_with_service_account()
```

Alternatively, you can explicitly pass the path to your service account key:

```python
from pathlib import Path

import myst

myst.authenticate_with_service_account(key_file_path=Path("/path/to/key/file.json"))
```

## Working with time series

Time series are at the core of Myst's API. To retrieve a time series by UUID:

```python
import myst

# You'll have to replace this UUID with the UUID of a time series you own.
time_series = myst.TimeSeries.get("ca2a63d1-3515-47b4-afc7-13c6656dd744")
```

You can insert a `TimeArray` into the time series:

```python
import myst
import numpy as np

time_array = myst.TimeArray(
    sample_period="PT1H",
    start_time="2021-07-01T00:00:00Z",
    end_time="2021-07-08T00:00:00Z",
    as_of_time="2021-07-01T00:00:00Z",
    values=np.random.randn(168),
)
time_series.insert_time_array(time_array=time_array)
```

You can also query a time series for a given as of time and natural time range. In this
example, the query should return the data we just inserted:

```python
import myst
from myst.testing import assert_time_array_equal

returned_time_array = time_series.query_time_array(
    start_time=myst.Time("2021-07-01T00:00:00Z"),
    end_time=myst.Time("2021-07-08T00:00:00Z"),
    as_of_time=myst.Time("2021-07-01T00:00:00Z"),
)
assert_time_array_equal(returned_time_array, time_array)
```

## Support

For questions or just to say hi, reach out to `support@myst.ai`.
