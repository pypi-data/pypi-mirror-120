# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wikipedia_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.13.0,<4.0.0',
 'requests>=2.26.0,<3.0.0',
 'types-requests>=2.25.6,<3.0.0']

entry_points = \
{'console_scripts': ['wikipedia-cli = wikipedia_cli.console:main']}

setup_kwargs = {
    'name': 'wikipedia-cli-by-ss',
    'version': '0.1.0',
    'description': 'A command-line application to retrieve random articles from Wikipedia.',
    'long_description': '[![Tests](https://github.com/SoheilSalmani/wikipedia-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/SoheilSalmani/wikipedia-cli/actions/workflows/tests.yml)\n[![codecov](https://codecov.io/gh/SoheilSalmani/wikipedia-cli/branch/master/graph/badge.svg?token=KG1NCKGY95)](https://codecov.io/gh/SoheilSalmani/wikipedia-cli)\n\n# Wikipedia CLI\n\nA command-line application to retrieve random articles from Wikipedia.\n',
    'author': 'Soheil Salmani',
    'author_email': 'salmani.soheil@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SoheilSalmani/wikipedia-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
