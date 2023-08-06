# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['licensegh']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.23,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'rich>=10.9.0,<11.0.0']

entry_points = \
{'console_scripts': ['licensegh = licensegh.cli:main']}

setup_kwargs = {
    'name': 'licensegh',
    'version': '0.1.3',
    'description': 'licensegh is a command line tool that generates a license file for a project from the github open source lincese templates',
    'long_description': '# licensegh\n\n<a href="https://github.com/sauljabin/licensegh/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/github/license/sauljabin/licensegh"></a>\n<a href="https://github.com/sauljabin/licensegh/actions/workflows/main.yml"><img alt="GitHub Actions" src="https://img.shields.io/github/checks-status/sauljabin/licensegh/main?label=tests"></a>\n<a href="https://app.codecov.io/gh/sauljabin/licensegh"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/sauljabin/licensegh"></a>\n<a href="https://pypi.org/project/licensegh/"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/licensegh"></a>\n<a href="https://pypi.org/project/licensegh/"><img alt="Version" src="https://img.shields.io/pypi/v/licensegh"></a>\n<a href="https://libraries.io/pypi/licensegh"><img alt="Dependencies" src="https://img.shields.io/librariesio/release/pypi/licensegh"></a>\n\n\n`licensegh` is a command line tool that generates a license file for a project from the github open source lincese templates\n\n## Installation\n\nIntall with pip:\n\n```sh\npip install licensegh\n```\n\nUpgrade with pip:\n```sh\npip install --upgrade licensegh\n```\n\n## Usage\n\nHelp `licensegh -h`:\n\n```sh\nUsage: licensegh [OPTIONS] <license id>\n\nOptions:\n  -p, --print   Print the license file\n  -s, --search  Search license, shows a list\n  -l, --list    List all found licenses\n  --version     Show the version and exit.\n  -h, --help    Show this message and exit.\n```\n\nList `licensegh -l`:\n\n![](screenshots/list.png)\n\nSearch `licensegh -s`:\n\n![](screenshots/search.png)\n\nPrint `licensegh -p`:\n\n![](screenshots/print.png)\n\nSave:\n\n```sh\nlicensegh mit\n```\n\n## Development\n\nInstall development tools:\n\n- make sure you have `python3.7`, `python3.8`, `python3.9` aliases installed\n- install [poetry](https://python-poetry.org/docs/#installation)\n\nInstalling development dependencies:\n\n```sh\npoetry install\n```\n\nRunning unit tests:\n\n```sh\npoetry run python -m scripts.tests\n```\n\nRunning multi version tests (`3.7`, `3.8`, `3.9`):\n\n```sh\npoetry run python -m scripts.multi-version-tests\n```\n\nApplying code styles:\n\n```sh\npoetry run python -m scripts.styles\n```\n\nRunning code analysis:\n\n```sh\npoetry run python -m scripts.analyze\n```\n\nRunning code coverage:\n\n```sh\npoetry run python -m scripts.tests-coverage\n```\n\nRunning cli using `poetry`:\n\n```sh\npoetry run licensegh\n```\n',
    'author': 'Saúl Piña',
    'author_email': 'sauljabin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sauljabin/licensegh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
