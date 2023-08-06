# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convert_to_queryset']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'convert-to-queryset',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'deepak',
    'author_email': 'info.deepakpatidar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
