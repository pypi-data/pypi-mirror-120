# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vankrupt_workshop_client']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['uploader_client = clients.console:main']}

setup_kwargs = {
    'name': 'vankrupt-workshop-client',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Vankrupt workshop clients\nHere you'll find reference implementations of clients \nfor interacting with vankrupt workshop APIs. \n\nThe library comes with CLI client for uploading mods, \nand a reference client for downloading/upgrading them. \n",
    'author': 'MeRuslan',
    'author_email': 'clanghopper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
