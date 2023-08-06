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
    'version': '0.2.0rc3',
    'description': 'Axial3D CLI',
    'long_description': "# A3D CLI #\n\nAccessing the Axial3D apis from the command line\n\n### Requirements\n\n* Python 3.7, 3.8, 3.9\n\n### Install\n\n    pip install a3d-cli\n\n#### Usage\n\nCreate an order:\n\n    a3dcli create --config_file config.json --dicom_location ./path_to_dicoms/ --order-type 3DPrint --notes notes --surgery 'Surgery' --patient-gender M --patient-birth-year 2001 --catalogue-item 101 --required-date '10-08-2021'\n\nUpdate an order\n\n    a3dcli upload --config_file config.json --dicom_location ./path_to_dicoms/ --order_id 1000\n\nView help:\n\n```\na3dcli --help\nusage: a3dcli [-h] --config_file CONFIG_FILE --order-type [ORDER_TYPES [ORDER_TYPES ...]] --catalogue-item-id [CATALOGUE_ITEM_ID] --surgery [SURGERY] --required-date [REQUIRED_DATE]\n              --patient-gender [{M,F,U}] --patient-birth-year [BIRTH_YEAR] --notes [NOTES] [--base_url BASE_URL] [--verify] [--username USERNAME] [--password PASSWORD] [--order_id ORDER_ID] [--dicom_location DICOM_LOCATION] {create,upload}\n\nAxial3D CLI (0.2.0)\n\npositional arguments:\n  {create,upload}\n                        Create Order, Upload by order id\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --config_file CONFIG_FILE\n                        a3dcli config file\n  --order-type [ORDER_TYPES [ORDER_TYPES ...]]\n                        Order Types\n  --catalogue-item-id [CATALOGUE_ITEM_ID]\n                        Catalogue Item\n  --surgery [SURGERY]   Surgery\n  --required-date [REQUIRED_DATE]\n                        Required Date\n  --patient-gender [{M,F,U}]\n                        Gender\n  --patient-birth-year [BIRTH_YEAR]\n                        Gender\n  --notes [NOTES]       Notes\n  --base_url BASE_URL   Base url of axial3D API\n  --verify\n  --username USERNAME   axial3D account username\n  --password PASSWORD   axial3D account password\n  --order_id ORDER_ID   ID of the order\n  --dicom_location DICOM_LOCATION\n                        Path to DICOM files\n```\n\n### Dev requirements\n\n* Poetry - https://python-poetry.org/\n* Tox - https://tox.readthedocs.io/\n\n### Build\n\n    poetry build\n\n### Testing\n\n#### Unit tests\n\n    poetry run pytest\n\n#### Integration tests\n\n    poetry run pytest --integration --integration-user USERNAME --integration-password PASSWORD --integration-url https://example.com\n\n### Build\n\n    poetry build\n\n    > Building a3d-cli (0.1.0)\n    > - Building sdist\n    > - Built a3d-cli-0.1.0.tar.gz\n    > - Building wheel\n    > - Built a3d_cli-0.1.0-py3-none-any.whl",
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
