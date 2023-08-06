# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_watcher']

package_data = \
{'': ['*']}

install_requires = \
['watchdog>=2.0.0']

entry_points = \
{'console_scripts': ['pytest_watcher = pytest_watcher:run']}

setup_kwargs = {
    'name': 'pytest-watcher',
    'version': '0.2.0',
    'description': 'Continiously watches for changes in your python files and runs pytest',
    'long_description': '# A simple watcher for pytest\n\n![PyPI](https://img.shields.io/pypi/v/pytest-watcher)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-watcher)\n![GitHub](https://img.shields.io/github/license/olzhasar/pytest-watcher)\n\n## Overview\n\n**pytest-watcher** is a tool to automatically rerun `pytest` whenever any `.py` file changes in your project.\nIt uses Linux [inotify API](https://man7.org/linux/man-pages/man7/inotify.7.html) for event monitoring via python [inotify library](https://pypi.org/project/inotify/).\n\n`pytest` invocation will be triggered when you change, delete or create new python files in watched directory.\n\n## Install pytest-watcher\n\n```\npip install pytest-watcher\n```\n\n## Usage\n\nSpecify the path that you want to watch:\n\n```\npytest-watcher .\n```\nor \n```\npytest-watcher /home/repos/project\n```\n\nAny additional arguments will be forwarded to `pytest`:\n```\npytest-watcher . -x --lf --nf\n```\n\n## Compatibility\n\nThis utility should be compatible with any Linux-based Operating System.\nBecause it relies on `inotify` API, using on MacOS or Windows is not currently possible.\n\nLibrary code is tested for Python versions 3.6+\n',
    'author': 'olzhasar',
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
