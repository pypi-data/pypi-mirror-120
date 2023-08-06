# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['node_py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'node-py',
    'version': '0.0.2',
    'description': 'Easy to use, package that brings aspects of node.js to python, but improvised and with new features.',
    'long_description': None,
    'author': 'Ryan Cundiff',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
