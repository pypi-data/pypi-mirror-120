# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indianapy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'indianapy',
    'version': '0.1.1',
    'description': 'Enforces the  Indiana Pi Bill',
    'long_description': 'This python modular enforces the correct value of math constant pi as per bill #246 of the 1897 sitting of the Indiana General Assembly.\n\nSimply `import indianapy` prior to usage.\n\nUse math.pi as usual.\n\n```python\n>>> import indianapy\n>>> import math\n>>> \n>>> print(math.pi)\n3.2\n>>> \n```',
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
