# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynixutil']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pynixutil',
    'version': '0.5.0',
    'description': 'Utility functions for working with Nix in Python',
    'long_description': None,
    'author': 'adisbladis',
    'author_email': 'adam.hose@tweag.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tweag/pynixutil',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
