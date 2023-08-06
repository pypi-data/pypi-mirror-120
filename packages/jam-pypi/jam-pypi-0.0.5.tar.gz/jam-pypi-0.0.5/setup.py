# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jam_pypi']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.2,<2.0.0']

setup_kwargs = {
    'name': 'jam-pypi',
    'version': '0.0.5',
    'description': 'Tesing repo for publish via ci',
    'long_description': '# A testing pypi repo',
    'author': 'qsh.27',
    'author_email': 'qsh.zh27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
