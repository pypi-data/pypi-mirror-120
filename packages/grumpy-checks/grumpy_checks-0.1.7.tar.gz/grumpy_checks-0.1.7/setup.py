# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grumpy_checks', 'grumpy_checks.cli']

package_data = \
{'': ['*'], 'grumpy_checks.cli': ['grumpy_report/*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'flake8>=3.9.2,<4.0.0',
 'pydocstyle>=6.1.1,<7.0.0',
 'rich>=10.9.0,<11.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['codecov = scripts:coverage_report',
                     'document = scripts:documentation',
                     'grumpy = grumpy_checks.application:main',
                     'test = scripts:test']}

setup_kwargs = {
    'name': 'grumpy-checks',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
