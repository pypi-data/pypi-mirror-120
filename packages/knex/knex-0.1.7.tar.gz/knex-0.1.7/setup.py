# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['knex']

package_data = \
{'': ['*']}

install_requires = \
['regex>=2021.8.28,<2022.0.0']

setup_kwargs = {
    'name': 'knex',
    'version': '0.1.7',
    'description': 'Python library for building composable text parsers',
    'long_description': '# KNEX\n\nPython library for creating chainable data transformers.\n\n## Installation\n\n`pip install knex`\n\n## Usage\n\n```python\n>>> from knex.parsers import *\n>>>\n>>> input_data = """\n... Interface             IP-Address      OK?    Method Status          Protocol\n... GigabitEthernet0/1    unassigned      YES    unset  up              up\n... GigabitEthernet0/2    192.168.190.235 YES    unset  up              up\n... GigabitEthernet0/3    unassigned      YES    unset  up              up\n... GigabitEthernet0/4    192.168.191.2   YES    unset  up              up\n... TenGigabitEthernet2/1 unassigned      YES    unset  up              up\n... Virtual36             unassigned      YES    unset  up              up\n... """\n>>>\n>>> pattern = r"\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b"\n>>>\n>>> result = (\n                Start(input_data)\n                > RegexExtractAll(pattern)\n                > GetIndex(0)\n                > Concat("", "/24")\n                > IpNetwork()\n             ).result\n>>>\n>>> print(result)\n192.168.190.0/24\n>>>\n\n```\n\n## Development\n\n### Environment Setup\n\n1. Install Poetry\n2. Clone the repo: `git clone https://github.com/clay584/knex && cd knex`\n3. Install pre-requisits for developement: `poetry install`\n4. Install PyPI API Key: `poetry config pypi-token.pypi <token>`\n5. Activate the environment: `poetry shell`\n6. Install git pre-commit hook: `pre-commit install && pre-commit autoupdate`\n\n### Publishing to PyPI\n\n1. Run tests and validate coverage: `pytest -v --cov=knex --cov-report html tests`\n2. Commit all changes, and have clean git repo on `main` branch.\n3. Bump version: `bump2version <major|minor|patch>`\n4. Push to git: `git push origin main --tags`\n5. Build for PyPI: `poetry build`\n6. Publish to PyPI: `poetry publish`\n',
    'author': 'Clay Curtis',
    'author_email': 'clay584@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/clay584/knex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
