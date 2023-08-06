# nadypy

A client library for accessing a [Nadybot](https://github.com/Nadybot/Nadybot)'s API.

## Installation

From PyPi:

```shell
pip install nadypy
```

From GitHub:

```shell
pip install git+https://github.com/Nadybot/nadypy.git
```

## Usage

First, create a client:

```python
from nadypy import Client

client = Client(base_url="http://localhost:8080/api")
```

If the endpoints you're going to hit require authentication (this currently applies to **all** endpoints), use either a `BasicAuthClient` or a `SignedAuthClient` instead.

`BasicAuthClient` uses credentials acquired via `!webauth`, which are not valid permanently:

```python
from nadypy import BasicAuthClient

client = BasicAuthClient(base_url="http://localhost:8080/api", username="Character", password="password")
```

`SignedAuthClient` uses private keys as explained [here](https://github.com/Nadybot/Nadybot/wiki/REST-API):

```python
from nadypy import SignedAuthClient

signed_auth_client = SignedAuthClient(
    "http://localhost:8080/api",
    key_id="bd879e20",
    private_key="""\
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEINca+XgCZoLXuu6p77cphsIxMiSaG09tBH6SV9AgEH4ioAoGCCqGSM49
AwEHoUQDQgAEPnzqwJq/el8kyNSPmYhQJ0L2qrMFtM3XDbAHrTQlXbFN2G8NmMBp
i52oubVjuTSHol1BQf4Haftbt0oBvHGUIw==
-----END EC PRIVATE KEY-----
""",
)
```

Now call your endpoint and use your models:

```python
from typing import Optional

from nadypy.models import SystemInformation
from nadypy.api.system import get_sysinfo
from nadypy.types import Response

sysinfo: Optional[SystemInformation] = get_sysinfo.sync(client=client)
# or if you need more info (e.g. status_code)
response: Response[SystemInformation] = get_sysinfo.sync_detailed(client=client)
```

Or do the same thing with an async version:

```python
from typing import Optional

from nadypy.models import SystemInformation
from nadypy.api.system import get_sysinfo
from nadypy.types import Response

sysinfo: Optional[SystemInformation] = await get_sysinfo.asyncio(client=client)
# or if you need more info (e.g. status_code)
response: Response[SystemInformation] = await get_sysinfo.asyncio_detailed(client=client)
```
