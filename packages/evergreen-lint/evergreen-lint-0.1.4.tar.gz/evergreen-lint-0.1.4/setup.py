# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evergreen_lint', 'evergreen_lint.rules']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.0.0', 'click>=7.0,<8.0', 'typing-extensions>=3.10.0,<4.0.0']

entry_points = \
{'console_scripts': ['main = evergreen_lint.__main__:main']}

setup_kwargs = {
    'name': 'evergreen-lint',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Richard Samuels',
    'author_email': 'richard.samuels@mongodb.com',
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
