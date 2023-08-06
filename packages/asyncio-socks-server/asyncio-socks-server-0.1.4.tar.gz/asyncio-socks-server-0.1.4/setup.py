# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncio_socks_server']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['asyncio_socks_server = '
                     'asyncio_socks_server.__main__:main']}

setup_kwargs = {
    'name': 'asyncio-socks-server',
    'version': '0.1.4',
    'description': 'A socks server implemented with asyncio.',
    'long_description': None,
    'author': 'Amaindex',
    'author_email': 'amaindex@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Amaindex/asyncio-socks-server',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
