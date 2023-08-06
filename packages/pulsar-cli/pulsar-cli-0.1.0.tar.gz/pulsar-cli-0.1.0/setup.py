# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pulsar_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'fastavro>=1.4.4,<2.0.0',
 'pulsar-client>=2.8.0,<3.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['pulse = pulse.main:main']}

setup_kwargs = {
    'name': 'pulsar-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Casey Mau',
    'author_email': 'cmau@overstock.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
