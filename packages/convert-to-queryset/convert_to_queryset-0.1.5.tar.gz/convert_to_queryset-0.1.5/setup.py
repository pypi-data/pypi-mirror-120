# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convert_to_queryset']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'convert-to-queryset',
    'version': '0.1.5',
    'description': 'library for convert list,tuple and dictionary into queryset',
    'long_description': '\n# convert to queryset\n\nThis package enables you to convert list,tuple and set into queryset\n\nTo install this package, use \n\n```bash\npip install convert-to-queryset\n```\n# for list \nimport it using the following\n```bash\nfrom convert import list_to_queryset\n```\n\nit will take two arguments: model and list\n```bash\nlist_to_queryset(model,list)\n```',
    'author': 'deepak',
    'author_email': 'info.deepakpatidar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DeepakDarkiee/convert_to_queryset.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
