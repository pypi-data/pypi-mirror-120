# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cardsec']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.8.0,<6.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['cardsec = cardsec.main:app']}

setup_kwargs = {
    'name': 'cardsec',
    'version': '0.0.1',
    'description': '',
    'long_description': 'Cardsec\nSecurity Solution for Cardano SPOs.',
    'author': 'Advait Joglekar',
    'author_email': 'advaitjoglekar@yahoo.in',
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
