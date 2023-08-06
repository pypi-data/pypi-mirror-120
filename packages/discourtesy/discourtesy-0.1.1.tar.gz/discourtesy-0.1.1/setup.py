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
    'version': '0.1.1',
    'description': 'A minimal framework to handle Discord interactions.',
    'long_description': '# Discourtesy\n\nDiscourtesy is a minimal framework to handle Discord interactions.\n\n## Installation\n\nDiscourtesy requires [Python 3.9][python-3.9] or higher.\n\nThe package is available on PyPi, so install it with `pip` or another dependency manager.\n\n```bash\npip install discourtesy\n```\n\n## Introduction\n\n```py\nimport discourtesy\n\napplication = discourtesy.Application()\n\npublic_key = ""\napplication.set_public_key(public_key)\n\n\n@discourtesy.command("beep")\nasync def beep_command(client, interaction):\n    return "boop"\n\n\napplication.add_plugin(__name__)\n```\n\n```bash\nuvicorn filename:application\n```\n\n[python-3.9]: <https://www.python.org/downloads/>\n',
    'author': 'Robin Mahieu',
    'author_email': 'robin.mahieu@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/robinmahieu/discourtesy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
