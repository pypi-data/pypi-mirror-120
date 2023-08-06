# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sec_package']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.9b0,<22.0', 'flake8>=3.9.2,<4.0.0']

setup_kwargs = {
    'name': 'sec-package',
    'version': '0.1.76',
    'description': '',
    'long_description': None,
    'author': 'sven',
    'author_email': 'sven.lauenroth@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
