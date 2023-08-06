# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brawl_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'pydantic>=1.8.2,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'brawl-api',
    'version': '0.0.1a4',
    'description': 'Python wrapper for the Brawl Stars API',
    'long_description': '# Brawl API\n\nPython wrapper for the Brawl Stars API\n\n## Installation\n\n`pip install brawl-api`',
    'author': 'Sebastian Marines',
    'author_email': 'sebastian0marines@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sebastianmarines/brawl_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
