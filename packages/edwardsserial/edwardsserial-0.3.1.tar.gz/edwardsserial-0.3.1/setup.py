# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edwardsserial', 'edwardsserial.tic']

package_data = \
{'': ['*']}

install_requires = \
['pyserial']

setup_kwargs = {
    'name': 'edwardsserial',
    'version': '0.3.1',
    'description': 'Python API implementing the serial protocoll from edwards vacuum.',
    'long_description': '# TIC\n\nPython object-oriented wrapper for the TIC Turbo- and Instrument Controller from Edwards (https://shop.edwardsvacuum.com/products/d39722000/view.aspx).',
    'author': 'Jan Petermann',
    'author_email': 'jpeterma@physnet.uni-hamburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/codingcoffeebean/edwardsserial',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
