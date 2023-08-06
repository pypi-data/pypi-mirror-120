# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cardsec']

package_data = \
{'': ['*']}

install_requires = \
['distro>=1.6.0,<2.0.0', 'psutil>=5.8.0,<6.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['cardsec = cardsec.main:app']}

setup_kwargs = {
    'name': 'cardsec',
    'version': '0.0.3',
    'description': 'System and Security Assesment Tool for Cardano SPOs.',
    'long_description': 'Cardsec\nSecurity Solution for Cardano SPOs.',
    'author': 'Advait Joglekar',
    'author_email': 'advaitjoglekar@yahoo.in',
    'maintainer': 'Advait Joglekar',
    'maintainer_email': 'advaitjoglekar@yahoo.in',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
