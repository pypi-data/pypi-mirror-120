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
{'console_scripts': ['analyze = scripts.tests:analyze',
                     'licensegh = licensegh.cli:main',
                     'multi-version-tests = scripts.tests:multi_version_tests',
                     'styles = scripts.styles:main',
                     'tests = scripts.tests:main',
                     'tests-coverage = scripts.tests:tests_coverage']}

setup_kwargs = {
    'name': 'licensegh',
    'version': '0.1.0',
    'description': 'licensegh is a command line tool that generates a license file for a project from the github open source lincese templates',
    'long_description': '# licensegh\n\n![GitHub](https://img.shields.io/github/license/sauljabin/licensegh)\n![GitHub branch checks state](https://img.shields.io/github/checks-status/sauljabin/licensegh/main?label=tests)\n![Codecov](https://img.shields.io/codecov/c/github/sauljabin/licensegh)\n\n`licensegh` is a command line tool that generates a license file for a project from the github open source lincese templates\n\n## Installation\n\n```sh\npip install licensegh\n```\n\n## Usage\n\nGenerate a LICENSE file from a github template (`mit` example):\n```sh\nlicensegh mit\n```\n\nHelp:\n```sh\nUsage: licensegh [OPTIONS] <license id>\n\nOptions:\n  -p, --print   Print the license file\n  -s, --search  Search license, shows a list\n  -l, --list    List all found licenses\n  --version     Show the version and exit.\n  -h, --help    Show this message and exit.\n```\n\n## Development\n\nInstall development tools:\n\n- make sure you have `python3.7`, `python3.8`, `python3.9` aliases installed\n- install [poetry](https://python-poetry.org/docs/#installation)\n\nInstalling development dependencies:\n```sh\npoetry install\n```\n\nRunning multi version tests (`3.7`, `3.8`, `3.9`):\n```sh\npoetry run multi-version-tests\n```\n\nRunning unit tests:\n```sh\npoetry run tests\n```\n\nRunning code analysis:\n```sh\npoetry run analyze\n```\n\nApplying code styles:\n```sh\npoetry run styles\n```\n\nRunning cli using `python3`:\n```sh\npython3 -m licensegh\n```\n\nRunning cli using `poetry`:\n```sh\npoetry run licensegh\n```\n\nRunniging code coverage:\n```sh\npoetry run tests-coverage\n```',
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
