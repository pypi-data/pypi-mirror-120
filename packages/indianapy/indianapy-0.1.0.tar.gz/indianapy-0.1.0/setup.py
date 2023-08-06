# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indianapy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'indianapy',
    'version': '0.1.0',
    'description': 'Enforces the  Indiana Pi Bill',
    'long_description': None,
    'author': 'Michaela',
    'author_email': 'git@michaela.lgbt',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
