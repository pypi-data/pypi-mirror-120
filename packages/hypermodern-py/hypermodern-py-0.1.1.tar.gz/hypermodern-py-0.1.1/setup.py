# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_py']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.8b0,<22.0',
 'click>=8.0.1,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.13.0,<4.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'nox>=2021.6.12,<2022.0.0',
 'opencv-python>=4.5.3,<5.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-py = hypermodern_py.console:main']}

setup_kwargs = {
    'name': 'hypermodern-py',
    'version': '0.1.1',
    'description': 'My hypermodern Python project',
    'long_description': '[![Tests](https://github.com/andridns/hypermodern-py/workflows/Tests/badge.svg)](https://github.com/andridns/hypermodern-py/actions?workflow=Tests)\n\n[![codecov](https://codecov.io/gh/andridns/hypermodern-py/branch/main/graph/badge.svg?token=16D51BG5O3)](https://codecov.io/gh/andridns/hypermodern-py)\n\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-py.svg)](https://pypi.org/project/hypermodern-py/)\n\n# hypermodern-py\n\nMy hypermodern python project.\n',
    'author': 'Andri Danusasmita',
    'author_email': 'andridsasmita@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andridns/hypermodern-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
