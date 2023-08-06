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
    'version': '0.1.1',
    'description': 'Unofficial library for MatteBOX API.',
    'long_description': '# python-mattebox\n\nUnofficial Python library for MatteBOX IPTV.\n\n## Installing\n\n```shell\n$ python -m pip install mattebox\n```\n\n## Usage\n\n```python\n>>> from mattebox import MatteBOX\n>>> mbox = MatteBOX(USERNAME, PASSWORD, DEVICE_ID, SUBSCRIPTION_CODE)\n```\n\n### Examples\n\n```python  \n>>> # get list of TV channels\n>>> channels = mbox.channels\n\n>>> # get list of programs on specified channel\n>>> programs = mbox.get_programs(channels[0])\n\n>>> # get recordings\n>>> recordings = mbox.recordings\n\n>>> # get stream URL for specified program/recording\n>>> stream = mbox.get_stream(programs[0])\n\n>>> # search for TV program\n>>> results = mbox.search("Masza i niedźwiedź")\n```\n',
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
