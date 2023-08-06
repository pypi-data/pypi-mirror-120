# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neuro_bump_version']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<8.1.0', 'poetry-semver>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['neuro-bump-version = neuro_bump_version.main:main']}

setup_kwargs = {
    'name': 'neuro-bump-version',
    'version': '21.9',
    'description': 'Bump version for Neu.ro projects',
    'long_description': '# neuro-bump-version\nBump neu-ro tag to the next version\n',
    'author': 'Andrew Svetlov',
    'author_email': 'andrew.svetlov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neuro-inc/neuro-bump-version',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
