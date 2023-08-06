# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_watcher']

package_data = \
{'': ['*']}

install_requires = \
['watchdog>=2.0.0']

entry_points = \
{'console_scripts': ['ptw = pytest_watcher:run',
                     'pytest-watcher = pytest_watcher:run']}

setup_kwargs = {
    'name': 'pytest-watcher',
    'version': '0.2.1',
    'description': 'Continiously runs pytest on changes in *.py files',
    'long_description': '# A simple watcher for pytest\n\n![PyPI](https://img.shields.io/pypi/v/pytest-watcher)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-watcher)\n![GitHub](https://img.shields.io/github/license/olzhasar/pytest-watcher)\n\n## Overview\n\n**pytest-watcher** is a tool to automatically rerun `pytest` when your code changes.\nIt looks for `*.py` files changes in a directory that you specify. `pytest` will be automatically invoked when you create new files and modify or delete existing.\n\n## Install pytest-watcher\n\n```\npip install pytest-watcher\n```\n\n## Usage\n\nSpecify the path that you want to watch:\n\n```\nptw .\n```\nor \n```\nptw /home/repos/project\n```\n\nAny additional arguments will be forwarded to `pytest`:\n```\nptw . -x --lf --nf\n```\n\n## Compatibility\n\nThe utility is OS independent and should work on any platform.\n\nCode is tested for Python versions 3.6+\n',
    'author': 'Olzhas Arystanov',
    'author_email': 'o.arystanov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/olzhasar/pytest-watcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
