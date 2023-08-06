# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['andyao', 'andyao.mdspliter.tree']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'andyao.mdspliter.tree',
    'version': '0.1.0',
    'description': 'Tree data structure for mdsplitter.',
    'long_description': None,
    'author': 'zen96285',
    'author_email': 'zen96285@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
