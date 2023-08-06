# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['a3d_cli']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['a3dcli = a3d_cli.cli:main']}

setup_kwargs = {
    'name': 'a3d-cli',
    'version': '0.2.0rc1',
    'description': 'Axial3D CLI',
    'long_description': None,
    'author': 'Axial3D',
    'author_email': 'opensource@axial3d.com',
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
