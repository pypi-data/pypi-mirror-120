# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaskade']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'rich>=10.9.0,<11.0.0']

entry_points = \
{'console_scripts': ['kaskade = kaskade.cli:main']}

setup_kwargs = {
    'name': 'kaskade',
    'version': '0.0.0',
    'description': 'kaskade is a terminal user interface for kafka',
    'long_description': '# kaskade\n\n<a href="https://github.com/sauljabin/kaskade/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/github/license/sauljabin/kaskade"></a>\n<a href="https://github.com/sauljabin/kaskade/actions"><img alt="GitHub Actions" src="https://img.shields.io/github/checks-status/sauljabin/kaskade/main?label=tests"></a>\n<a href="https://app.codecov.io/gh/sauljabin/kaskade"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/sauljabin/kaskade"></a>\n<a href="https://pypi.org/project/kaskade"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/kaskade"></a>\n<a href="https://pypi.org/project/kaskade"><img alt="Version" src="https://img.shields.io/pypi/v/kaskade"></a>\n<a href="https://libraries.io/pypi/kaskade"><img alt="Dependencies" src="https://img.shields.io/librariesio/release/pypi/kaskade"></a>\n<a href="https://pypi.org/project/kaskade"><img alt="Platform" src="https://img.shields.io/badge/platform-linux%20%7C%20osx-blueviolet"></a>\n\n`kaskade` is a terminal user interface for [kafka](https://kafka.apache.org/).\n\n## Installation\n\nInstall with pip:\n```sh\npip install kaskade\n```\n\nUpgrade with pip:\n```sh\npip install --upgrade kaskade\n```\n\n## Usage\n\nHelp:\n```sh\nkaskade --help\n```\n\nVersion:\n```sh\nkaskade --version\n```\n\n## Development\n\nInstalling poetry:\n```sh\npip install poetry\n```\n\nInstalling development dependencies:\n```sh\npoetry install\n```\n\nRunning unit tests:\n```sh\npoetry run python -m scripts.tests\n```\n\nRunning multi version tests (`3.7`, `3.8`, `3.9`):\n\n> Make sure you have `python3.7`, `python3.8`, `python3.9` aliases installed\n\n```sh\npoetry run python -m scripts.multi-version-tests\n```\n\nApplying code styles:\n```sh\npoetry run python -m scripts.styles\n```\n\nRunning code analysis:\n```sh\npoetry run python -m scripts.analyze\n```\n\nRunning code coverage:\n```sh\npoetry run python -m scripts.tests-coverage\n```\n\nRunning cli using `poetry`:\n```sh\npoetry run kaskade\n```\n',
    'author': 'Saúl Piña',
    'author_email': 'sauljabin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sauljabin/kaskade',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
