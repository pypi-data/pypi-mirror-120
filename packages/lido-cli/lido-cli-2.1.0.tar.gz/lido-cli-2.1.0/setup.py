# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lido-node-operator-key-checker-cli']

package_data = \
{'': ['*'],
 'lido-node-operator-key-checker-cli': ['.git/*',
                                        '.git/hooks/*',
                                        '.git/info/*',
                                        '.git/logs/*',
                                        '.git/logs/refs/heads/*',
                                        '.git/logs/refs/remotes/origin/*',
                                        '.git/logs/refs/remotes/origin/feature/*',
                                        '.git/objects/00/*',
                                        '.git/objects/01/*',
                                        '.git/objects/09/*',
                                        '.git/objects/10/*',
                                        '.git/objects/1a/*',
                                        '.git/objects/26/*',
                                        '.git/objects/27/*',
                                        '.git/objects/28/*',
                                        '.git/objects/2b/*',
                                        '.git/objects/32/*',
                                        '.git/objects/37/*',
                                        '.git/objects/3c/*',
                                        '.git/objects/3e/*',
                                        '.git/objects/40/*',
                                        '.git/objects/41/*',
                                        '.git/objects/45/*',
                                        '.git/objects/5e/*',
                                        '.git/objects/61/*',
                                        '.git/objects/6a/*',
                                        '.git/objects/70/*',
                                        '.git/objects/76/*',
                                        '.git/objects/77/*',
                                        '.git/objects/7d/*',
                                        '.git/objects/7f/*',
                                        '.git/objects/85/*',
                                        '.git/objects/8d/*',
                                        '.git/objects/95/*',
                                        '.git/objects/9c/*',
                                        '.git/objects/a6/*',
                                        '.git/objects/a7/*',
                                        '.git/objects/b2/*',
                                        '.git/objects/b7/*',
                                        '.git/objects/b9/*',
                                        '.git/objects/ba/*',
                                        '.git/objects/cb/*',
                                        '.git/objects/cd/*',
                                        '.git/objects/db/*',
                                        '.git/objects/e0/*',
                                        '.git/objects/e6/*',
                                        '.git/objects/e7/*',
                                        '.git/objects/f4/*',
                                        '.git/objects/f9/*',
                                        '.git/objects/fa/*',
                                        '.git/objects/pack/*',
                                        '.git/refs/heads/*',
                                        '.git/refs/remotes/origin/*',
                                        '.git/refs/remotes/origin/feature/*',
                                        '.github/workflows/*']}

install_requires = \
['click==8.0.1', 'colorama==0.4.4', 'lido-sdk==2.2.1']

entry_points = \
{'console_scripts': ['lido-cli = lido_validate_keys:cli']}

setup_kwargs = {
    'name': 'lido-cli',
    'version': '2.1.0',
    'description': 'Lido CLI tool for node operator key validation',
    'long_description': '# <img src="https://docs.lido.fi/img/logo.svg" alt="Lido" width="46"/>\u2003Node Operator Key Checker CLI\n\n## Installation\n\nYou can get this tool using `pip`:\n\n```\npip install lido-cli\n```\n\nOr if you cloned this repository, install Python dependencies via:\n\n```\n./init.sh\n```\n\nDepending on how it\'s installed use:\n\n`lido-cli ...opts command ...opts` or `python lido_validate_keys.py ...opts command ...opts`\n\n## Running\n\n### RPC Provider\n\nThis is the only thing required, the rest will be handled automatically unless overridden.\n\n```\nlido-cli --rpc https://mainnet.provider.io/v3/XXX validate_network_keys\n```\n\n### Optional Parameters\n\nBy default, CLI will use embedded strings and ABIs, but you can specify your own arguments if needed. Make sure to use them on CLI itself and not on the command eg:\n\n```\nlido-cli --rpc https://mainnet.provider.io/v3/XXX --multicall_max_bunch 100 --multicall_max_workers 3 --multicall_max_retries 5 validate_network_keys\n```\n\n```\n--rpc                               RPC provider for network calls.\n--multicall_max_bunch               Max bunch amount of Calls in one Multicall (max recommended 300).\n--multicall_max_workers             Max parallel calls for multicalls.\n--multicall_max_retries             Max call retries.\n-d --details                        More logs about node operators and keys. (only for validate_network_keys)\n```\n\n### Checking Network Keys\n\nCommand: `validate_network_keys`\n\nExample:\n\n```\nlido-cli --rpc https://mainnet.provider.io/v3/XXX validate_network_keys\n```\n\n### Checking Keys from File\n\nCommand: `validate_file_keys`\nSpecify the input file via `--file`\n\nExample:\n\n```\nlido-cli --rpc https://mainnet.provider.io/v3/XXX validate_file_keys --file input.json\n```\n\n### ---\n\nYou can also get all commands and options via `python lido_validate_keys.py --help`\n',
    'author': 'Lido',
    'author_email': 'info@lido.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lido.fi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.7.1,<4',
}


setup(**setup_kwargs)
