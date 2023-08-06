# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ardlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ardlib',
    'version': '0.1.0',
    'description': 'ardlib',
    'long_description': None,
    'author': 'musangtara',
    'author_email': 'musangtara@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
