# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pass_addy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['run = password_manager.main:main']}

setup_kwargs = {
    'name': 'pass-addy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'addyR',
    'author_email': 'adarsharegmi121@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
