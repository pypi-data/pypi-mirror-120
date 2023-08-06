# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discourtesy', 'discourtesy.routes', 'discourtesy.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.4.0,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'starlette>=0.16.0,<0.17.0',
 'uvicorn>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'discourtesy',
    'version': '0.1.0',
    'description': 'A minimal framework to handle Discord interactions.',
    'long_description': None,
    'author': 'Robin Mahieu',
    'author_email': 'robin.mahieu@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
