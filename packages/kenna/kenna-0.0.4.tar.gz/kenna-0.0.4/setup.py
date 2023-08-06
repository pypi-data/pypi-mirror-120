# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kenna',
 'kenna.cli',
 'kenna.cli.command_groups',
 'kenna.data',
 'kenna.data.constants',
 'kenna.data.types']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'hodgepodge>=0.1.7,<0.2.0']

entry_points = \
{'console_scripts': ['kenna = kenna.cli:cli']}

setup_kwargs = {
    'name': 'kenna',
    'version': '0.0.4',
    'description': '',
    'long_description': "# Kenna\n\n> An API client for Kenna Security\n\n![Kenna](https://raw.githubusercontent.com/whitfieldsdad/images/main/kenna-hero.png)\n\n## Installation\n\nTo install using `pip`:\n\n```shell\n$ pip install kenna\n```\n\nTo install from source using `poetry`\n\n```shell\n$ git clone git@github.com:whitfieldsdad/python-kenna-api-client.git\n$ poetry install\n```\n\nTo install from source using `setup.py`:\n\n```shell\n$ git clone git@github.com:whitfieldsdad/python-kenna-api-client.git\n$ python3 setup.py install\n```\n\n## Required environment variables\n\nThe following environment variables are required:\n- `$KENNA_API_KEY`\n\n## Tutorials\n\nThe following general options are available:\n\n```shell\n$ poetry run kenna\nUsage: kenna [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --api-key TEXT\n  --region TEXT\n  --help          Show this message and exit.\n\nCommands:\n  applications\n  assets\n  connector-runs\n  connectors\n  dashboard-groups\n  fixes\n  roles\n  users\n  vulnerabilities\n```\n\nIf you're not using `poetry`, you can access the command line interface as follows:\n\n```shell\n$ python3 -m kenna.cli\n```\n\n### Applications\n\nThe following options are available when listing applications.\n\n```shell\n$ poetry run kenna applications\nUsage: kenna applications [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --application-ids TEXT\n  --application-names TEXT\n  --help                    Show this message and exit.\n\nCommands:\n  count-applications\n  get-applications\n```\n\n### Assets\n\nThe following options are available when listing assets: \n\n```shell\n$ poetry run kenna assets\nUsage: kenna assets [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --asset-ids TEXT\n  --asset-names TEXT\n  --help              Show this message and exit.\n\nCommands:\n  count-assets\n  get-assets\n```\n\n### Connectors\n\nThe following options are available when listing connectors:\n\n```shell\n$ poetry run kenna connectors\nUsage: kenna connectors [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  count-connectors\n  get-connectors\n```\n\n### Dashboard groups\n\nThe following options are available when listing dashboard groups:\n\n```shell\n$ poetry run kenna dashboard-groups\nUsage: kenna dashboard-groups [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  count-dashboard-groups\n  get-dashboard-groups\n```\n\n### Fixes\n\nThe following options are available when listing fixes:\n\n```shell\n$ poetry run kenna fixes\nUsage: kenna fixes [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  count-fixes\n  get-fixes\n```\n\n### Users\n\nThe following options are available when listing users:\n\n```shell\n$ poetry run kenna users\nUsage: kenna users [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  count-users\n  get-users\n```\n\n### Vulnerabilities\n\nThe following options are available when listing vulnerabilities:\n\n```shell\n$ poetry run kenna vulnerabilities\nUsage: kenna vulnerabilities [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  count-vulnerabilities\n  get-cves\n  get-vulnerabilities\n```\n",
    'author': 'Tyler Fisher',
    'author_email': 'tylerfisher@tylerfisher.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4',
}


setup(**setup_kwargs)
