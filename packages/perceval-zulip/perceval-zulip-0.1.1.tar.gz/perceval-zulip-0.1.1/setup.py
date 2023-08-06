# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perceval', 'perceval.backends', 'perceval.backends.zulip', 'tests']

package_data = \
{'': ['*'], 'tests': ['data/zulip/*']}

install_requires = \
['grimoirelab-toolkit', 'perceval', 'requests>=2.7.0,<3.0.0']

setup_kwargs = {
    'name': 'perceval-zulip',
    'version': '0.1.1',
    'description': 'Perceval backend for Zulip.',
    'long_description': '# perceval-zulip\n[![Build Status](https://github.com/vchrombie/grimoirelab-perceval-zulip/workflows/tests/badge.svg)](https://github.com/vchrombie/grimoirelab-perceval-zulip/actions?query=workflow:tests+branch:master+event:push) [![Coverage Status](https://img.shields.io/coveralls/vchrombie/grimoirelab-perceval-zulip.svg)](https://coveralls.io/r/vchrombie/grimoirelab-perceval-zulip?branch=master) [![PyPI version](https://badge.fury.io/py/perceval-zulip.svg)](https://badge.fury.io/py/perceval-zulip)\n\nPerceval backend for Zulip.\n\n## Requirements\n\n* Python >= 3.6.1\n* python3-requests >= 2.7\n* grimoirelab-toolkit >= 0.2\n* perceval >= 0.17.4\n\n## Installation\n\n### 1. PyPI\n\nPerceval Zulip backend can be installed using [pip](https://pip.pypa.io/en/stable/)\n```\n$ pip install perceval-zulip\n```\n\n### 2. Getting the source code\n\nClone the repository\n```\n$ git clone https://github.com/vchrombie/grimoirelab-perceval-zulip\n```\n\n### Prerequisites\n\n#### Poetry\n\nWe use [Poetry](https://python-poetry.org/docs/) for managing the project.\nYou can install it following [these steps](https://python-poetry.org/docs/#installation).\n\n### Setup\n\nInstall the required dependencies (this will also create a virtual environment)\n```\n$ poetry install\n```\n\nActivate the virtual environment\n```\n$ poetry shell\n```\n\n## Usage\n\n**Note:** You need the `email` and the `api_token` (API key) from the server. You can use the user email and API key\nfor authentication or create a bot and use the bot email and API key.\n\nReference: [About bots (Zulip Help Center)](https://zulip.com/help/bots-and-integrations).\n```\n(.venv) $ perceval zulip --help\n[2021-09-20 15:57:22,523] - Sir Perceval is on his quest.\nusage: perceval [-h] [--category CATEGORY] [--tag TAG] [--filter-classified] -t API_TOKEN\n                [--archive-path ARCHIVE_PATH] [--no-archive] [--fetch-archive]\n                [--archived-since ARCHIVED_SINCE] [--no-ssl-verify] [-o OUTFILE]\n                [--json-line] -e EMAIL\n                url stream\n\npositional arguments:\n  url                   Zulip chat URL\n  stream                Zulip chat stream name\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nauthentication arguments:\n  -t API_TOKEN, --api-token API_TOKEN\n                        backend authentication token / API key\n\nzulip arguments:\n  -e EMAIL, --email EMAIL\n                        Zulip bot/user email\n```\n\nFetch messages from the `importlib` stream of the [Python Zulip Server](https://python.zulipchat.com) with the\nbot email `bot@zulipchat.com` and API key `xxxx`\n```\n(.venv) $ perceval zulip https://python.zulipchat.com importlib -e bot@zulipchat.com -t xxxx\n[2021-09-20 15:59:24,593] - Sir Perceval is on his quest.\n{\n...\n```\n\n## Contributing\n\nThis project follows the [contributing guidelines](https://github.com/chaoss/grimoirelab/blob/master/CONTRIBUTING.md)\nof the GrimoireLab.\n\n## Acknowledgment\n\nThe backend was initially developed by [@vchrombie](https://github.com/vchrombie).\n\nAdhering to the guidelines, the work is started in this external repository. But, this can be merged\n([chaoss/grimoirelab-perceval/#/667](https://github.com/chaoss/grimoirelab-perceval/pull/667)) into the \n[Perceval](https://github.com/chaoss/grimoirelab-perceval) repository in the future.\n\n## License\n\nLicensed under GNU General Public License (GPL), version 3 or later.\n',
    'author': 'GrimoireLab Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://chaoss.github.io/grimoirelab/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
