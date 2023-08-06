# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccloud_cli_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ccloud-cli-api',
    'version': '0.0.1',
    'description': 'Simple wrapper around CCLoud CLI',
    'long_description': '==============\nccloud-cli-api\n==============\n\n\n.. image:: https://img.shields.io/pypi/v/ccloud_cli_api.svg\n        :target: https://pypi.python.org/pypi/ccloud_cli_api\n\nSimple wrapper around CCloud CLI to perform simple operation unavailable via API.\n\n\n* Free software: GNU General Public License v2\n* Documentation: https://ccloud-cli-api.readthedocs.io.\n\n\nFeatures\n--------\n\n* Allows to create API Keys for Service Account / Resource\n* List all clusters\n\n.. warning:: Requires ccloud installed to run subproccess commands.\n\n',
    'author': 'johnpreston',
    'author_email': 'john@compose-x.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
