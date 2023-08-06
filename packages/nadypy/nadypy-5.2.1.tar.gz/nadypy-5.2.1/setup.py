# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nadypy',
 'nadypy.api',
 'nadypy.api.audit',
 'nadypy.api.config',
 'nadypy.api.guild',
 'nadypy.api.messages',
 'nadypy.api.news',
 'nadypy.api.online',
 'nadypy.api.preferences',
 'nadypy.api.relay',
 'nadypy.api.system',
 'nadypy.api.webserver',
 'nadypy.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<22.0.0',
 'httpx>=0.15.4,<0.20.0',
 'pyopenssl>=20.0.1,<21.0.0',
 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'nadypy',
    'version': '5.2.1',
    'description': "A client library for accessing a Nadybot's API",
    'long_description': '# nadypy\n\nA client library for accessing a [Nadybot](https://github.com/Nadybot/Nadybot)\'s API.\n\n## Installation\n\nFrom PyPi:\n\n```shell\npip install nadypy\n```\n\nFrom GitHub:\n\n```shell\npip install git+https://github.com/Nadybot/nadypy.git\n```\n\n## Usage\n\nFirst, create a client:\n\n```python\nfrom nadypy import Client\n\nclient = Client(base_url="http://localhost:8080/api")\n```\n\nIf the endpoints you\'re going to hit require authentication (this currently applies to **all** endpoints), use either a `BasicAuthClient` or a `SignedAuthClient` instead.\n\n`BasicAuthClient` uses credentials acquired via `!webauth`, which are not valid permanently:\n\n```python\nfrom nadypy import BasicAuthClient\n\nclient = BasicAuthClient(base_url="http://localhost:8080/api", username="Character", password="password")\n```\n\n`SignedAuthClient` uses private keys as explained [here](https://github.com/Nadybot/Nadybot/wiki/REST-API):\n\n```python\nfrom nadypy import SignedAuthClient\n\nsigned_auth_client = SignedAuthClient(\n    "http://localhost:8080/api",\n    key_id="bd879e20",\n    private_key="""\\\n-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEINca+XgCZoLXuu6p77cphsIxMiSaG09tBH6SV9AgEH4ioAoGCCqGSM49\nAwEHoUQDQgAEPnzqwJq/el8kyNSPmYhQJ0L2qrMFtM3XDbAHrTQlXbFN2G8NmMBp\ni52oubVjuTSHol1BQf4Haftbt0oBvHGUIw==\n-----END EC PRIVATE KEY-----\n""",\n)\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom typing import Optional\n\nfrom nadypy.models import SystemInformation\nfrom nadypy.api.system import get_sysinfo\nfrom nadypy.types import Response\n\nsysinfo: Optional[SystemInformation] = get_sysinfo.sync(client=client)\n# or if you need more info (e.g. status_code)\nresponse: Response[SystemInformation] = get_sysinfo.sync_detailed(client=client)\n```\n\nOr do the same thing with an async version:\n\n```python\nfrom typing import Optional\n\nfrom nadypy.models import SystemInformation\nfrom nadypy.api.system import get_sysinfo\nfrom nadypy.types import Response\n\nsysinfo: Optional[SystemInformation] = await get_sysinfo.asyncio(client=client)\n# or if you need more info (e.g. status_code)\nresponse: Response[SystemInformation] = await get_sysinfo.asyncio_detailed(client=client)\n```\n',
    'author': 'Jens Reidel',
    'author_email': 'adrian@travitia.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Nadybot/nadypy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
