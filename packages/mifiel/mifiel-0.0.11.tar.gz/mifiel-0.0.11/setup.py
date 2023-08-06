# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mifiel', 'mifiel.api_auth']

package_data = \
{'': ['*']}

install_requires = \
['cookies>=2.2.1,<3.0.0',
 'nose2>=0.10.0,<0.11.0',
 'requests>=2.20.0',
 'responses>=0.9.0,<0.10.0',
 'unittest2>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'mifiel',
    'version': '0.0.11',
    'description': 'Python API Client library for mifiel.com',
    'long_description': None,
    'author': 'Genaro Madrid',
    'author_email': 'genmadrid@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
