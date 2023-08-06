# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ways_py']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.9.2,<4.0.0',
 'importlib-metadata>=4.8.1,<5.0.0',
 'mypy>=0.910,<0.911',
 'pytest>=6.2.5,<7.0.0']

setup_kwargs = {
    'name': 'ways-py',
    'version': '0.0.2',
    'description': 'WAYS package for Python developed at University of Warwick and The Alan Turing Institute.',
    'long_description': None,
    'author': 'Ed Chalstrey',
    'author_email': 'echalstrey@turing.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
