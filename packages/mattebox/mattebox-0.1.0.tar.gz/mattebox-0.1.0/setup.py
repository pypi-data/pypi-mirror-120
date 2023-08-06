# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mattebox']

package_data = \
{'': ['*']}

install_requires = \
['m3u8>=0.9.0,<0.10.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'mattebox',
    'version': '0.1.0',
    'description': 'Unofficial library for MatteBOX API.',
    'long_description': None,
    'author': 'samedamci',
    'author_email': 'samedamci@disroot.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.2,<4.0.0',
}


setup(**setup_kwargs)
