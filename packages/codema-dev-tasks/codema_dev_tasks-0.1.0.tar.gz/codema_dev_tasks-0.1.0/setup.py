# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codema_dev_tasks']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'fsspec>=2021.8.1,<2022.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'codema-dev-tasks',
    'version': '0.1.0',
    'description': 'A collection of Python helper functions for use in ETL pipelines',
    'long_description': None,
    'author': 'Rowan Molony',
    'author_email': 'rowan.molony@codema.ie',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
