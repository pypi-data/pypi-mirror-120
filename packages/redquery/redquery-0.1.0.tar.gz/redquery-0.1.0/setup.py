# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redquery']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.18.43,<2.0.0',
 'documented>=0.1.1,<0.2.0',
 'mypy-boto3-redshift-data>=1.18.43,<2.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['redquery = redquery.cli:app']}

setup_kwargs = {
    'name': 'redquery',
    'version': '0.1.0',
    'description': 'Run SQL queries against AWS Redshift via its Data API.',
    'long_description': None,
    'author': 'Anatoly Scherbakov',
    'author_email': 'altaisoft@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
