# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['treeo']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.2.18,<0.3.0', 'jaxlib>=0.1.70,<0.2.0']

setup_kwargs = {
    'name': 'treeo',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
