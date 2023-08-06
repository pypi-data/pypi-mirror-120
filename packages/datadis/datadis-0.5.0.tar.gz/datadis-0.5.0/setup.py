# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datadis']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'datadis',
    'version': '0.5.0',
    'description': 'Datadis API client',
    'long_description': '# Datadis\nAPI client for https://datadis.es\n\n[![Semantic Release](https://github.com/MrMarble/datadis/actions/workflows/release.yml/badge.svg)](https://github.com/MrMarble/datadis/actions/workflows/release.yml)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/datadis)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MrMarble_datadis&metric=alert_status)](https://sonarcloud.io/dashboard?id=MrMarble_datadis)\n\n',
    'author': 'Alvaro Tinoco',
    'author_email': 'alvarotinocomarmol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
