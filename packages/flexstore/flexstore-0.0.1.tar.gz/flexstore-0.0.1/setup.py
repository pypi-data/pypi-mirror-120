# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flexstore', 'flexstore.storage_providers']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.84,<2.0.0', 'msgpack>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'flexstore',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Dan Sikes',
    'author_email': 'dansikes7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
