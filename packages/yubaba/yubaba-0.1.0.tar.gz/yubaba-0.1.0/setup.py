# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yubaba']

package_data = \
{'': ['*']}

install_requires = \
['single-source>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'yubaba',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'edge-minato',
    'author_email': 'edge.minato@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
