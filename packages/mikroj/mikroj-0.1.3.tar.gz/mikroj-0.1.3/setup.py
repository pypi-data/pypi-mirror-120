# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mikroj', 'mikroj.implementations', 'mikroj.macros', 'mikroj.registries']

package_data = \
{'': ['*']}

install_requires = \
['pyimagej>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['mikroj = mikroj.run:main']}

setup_kwargs = {
    'name': 'mikroj',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
