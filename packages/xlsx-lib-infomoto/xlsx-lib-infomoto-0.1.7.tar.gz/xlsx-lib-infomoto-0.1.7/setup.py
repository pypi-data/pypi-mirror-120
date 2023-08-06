# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['base_model']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl-image-loader>=1.0.5,<2.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'xlsx-lib-infomoto',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'tomasdarioam',
    'author_email': 'tomasdarioam@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
