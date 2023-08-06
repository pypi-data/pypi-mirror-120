# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['main_package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'main-package',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'sven',
    'author_email': 'sven.lauenroth@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
