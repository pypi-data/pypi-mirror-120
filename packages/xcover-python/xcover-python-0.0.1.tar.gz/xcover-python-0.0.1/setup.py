# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xcover']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26,<3.0']

setup_kwargs = {
    'name': 'xcover-python',
    'version': '0.0.1',
    'description': 'Python client for XCover API (XCore).',
    'long_description': '# XCover SDK for Python\n\nXCover SDK is a Python package that simplifies XCover API integration.\n\n# Installation \n\nXCover SDK is available on PyPI. \nYou can use the following commands to install the latest version:\n\n    pip install xcover\n\nor \n\n    poertry install xcover \n\n# Features\n\n- Authentication\n- Simple configuration using env variables\n\n# Configuration\n\n## Config object\n\nThe library provides `XCoverConfig` dataclass that can be used as following:\n\n```python\nfrom xcover import XCover, XCoverConfig\n\nclient = XCover(\n    XCoverConfig( # minimal config, check autocomplete for more options\n        base_url="https://api.xcover.com/xcover",\n        partner_code="--PARTNER_CODE--",\n        auth_api_key="--API_KEY--",\n        auth_api_secret="--API_SECRET--",\n    )\n)\n\n```\n\n## Env variables\n\nAlternatively, the library can be configured using env variables. \n\nThe full list of config options is below:\n\n* `XC_BASE_URL` (`XCoverConfig.base_url`): XCover base URL (e.g. `https://api.xcover.com/api/v2/`). \n* `XC_PARTNER_CODE` (`XCoverConfig.partner_code`): Partner code (e.g. `LLODT`).\n* `XC_HTTP_TIMEOUT` (`XCoverConfig.http_timeout`): HTTP timeout in seconds. Default value is `10`. \n* `XC_AUTH_API_KEY` (`XCoverConfig.auth_api_key`): API key to use.\n* `XC_AUTH_API_SECRET` (`XCoverConfig.auth_api_secret`): API secret to use.\n* `XC_AUTH_ALGORITHM` (`XCoverConfig.auth_algorithm`): HMAC encoding algorithm to use. Default is `hmac-sha512`.\n* `XC_AUTH_HEADERS` (`XCoverConfig.auth_headers`): Headers to sign. Default is `(request-target) date`.\n\n# Usage example\n\n## Using `call` method\n\n```python\nimport requests\n\nfrom xcover.xcover import XCover\n\n# Env variables are used\nclient = XCover()\n\n# Prepare payload\npayload = {\n    "request": [\n        {\n            "policy_type": "event_ticket_protection",\n            "policy_type_version": 1,\n            "policy_start_date": "2021-12-01T17:59:00.831+00:00",\n            "event_datetime": "2021-12-25T21:00:00+00:00",\n            "event_name": "Ariana Grande",\n            "event_location": "The O2",\n            "number_of_tickets": 2,\n            "tickets": [\n                {"price": 100},\n            ],\n            "resale_ticket": False,\n            "event_country": "GB",\n        }\n    ],\n    "currency": "GBP",\n    "customer_country": "GB",\n    "customer_region": "London",\n    "customer_language": "en",\n}\n# Calling XCover API\nresponse = client.call(\n    method="POST",\n    url="partners/LLODT/quotes/",\n    payload=payload,\n)\n\nquote: requests.Response = response.json()\n```\n',
    'author': 'Artem Kolesnikov',
    'author_email': 'artem@covergenius.com',
    'maintainer': 'Artem Kolesnikov',
    'maintainer_email': 'artem@covergenius.com',
    'url': 'https://www.covergenius.com/xcover/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
