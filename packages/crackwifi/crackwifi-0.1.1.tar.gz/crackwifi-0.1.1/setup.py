# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crackwifi']

package_data = \
{'': ['*']}

install_requires = \
['plumbum>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'crackwifi',
    'version': '0.1.1',
    'description': 'Automate cracking wifis using reaver',
    'long_description': '# crackwifi\n\n![crackwifi.png](https://raw.githubusercontent.com/4thel00z/logos/master/crackwifi.png)\n\n## Motivation\n\nI am stupid hägger and do not want to have to remember reaver specific commands to hack noobs.\n\n## Installation\n\n```shell\npip install crackwifi\n```\n\n## Usage\n\n```python\nfrom crackwifi import dump_networks, monitor\n\nif __name__ == \'__main__\':\n    with monitor("wlx6cfdb9b29a25"):\n        networks = dump_networks(10)\n\tfirst = list(networks.values())[0]\n\tfor progress in first.attack():\n\t\tprint(progress)\n```\n\n## License\n\nThis project is licensed under the GPL-3 license.\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4thel00z/crackwifi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
