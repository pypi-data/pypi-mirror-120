# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commitexplorer']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'requests-cache>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'commit-explorer-client',
    'version': '0.2.0',
    'description': 'Client for Commit Explorer',
    'long_description': None,
    'author': 'hlib',
    'author_email': 'hlibbabii@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
