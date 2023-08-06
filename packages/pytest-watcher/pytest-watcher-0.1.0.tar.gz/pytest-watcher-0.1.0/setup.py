# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_watcher']

package_data = \
{'': ['*']}

install_requires = \
['inotify>=0.2.10,<0.3.0']

entry_points = \
{'console_scripts': ['pytest_watcher = pytest_watcher:run']}

setup_kwargs = {
    'name': 'pytest-watcher',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'olzhasar',
    'author_email': 'o.arystanov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
