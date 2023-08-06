# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['milkyway_sdk']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.4.8,<4.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'requests>=2.26.0,<3.0.0',
 'terra_sdk>=1.0.0-b2,<2.0.0']

setup_kwargs = {
    'name': 'milkyway-sdk',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Stargazer 838',
    'author_email': 'stargazers838@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
