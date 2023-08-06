# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongodb_bundle']

package_data = \
{'': ['*']}

install_requires = \
['applauncher>=2.0.0,<3.0.0', 'pymongo>=3.11.3,<4.0.0']

setup_kwargs = {
    'name': 'mongodb-bundle',
    'version': '2.1.0',
    'description': 'Mongodb support for applauncher',
    'long_description': None,
    'author': 'Alvaro Garcia',
    'author_email': 'maxpowel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
