# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycommandparse', 'pycommandparse.parsers']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.9b0,<22.0']

setup_kwargs = {
    'name': 'pycommandparse',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'thelegendbeacon',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
