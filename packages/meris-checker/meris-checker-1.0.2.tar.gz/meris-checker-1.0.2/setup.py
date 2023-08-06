# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meris_checker']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['meris-checker = meris_checker:main']}

setup_kwargs = {
    'name': 'meris-checker',
    'version': '1.0.2',
    'description': 'A script which checks the qrator database to see if any of your IPs is listed as part of the Meris botnet.',
    'long_description': '# meris-checker\n\nmeris-checker is a command which helps you determine whether or not your IP addresses are listed in the Qrator Labs database of meris botnet IPs.\n\n## Installation\n\nUse the package manager [poetry](https://python-poetry.org/docs/) to install meris-checker.\n\n```bash\npoetry install meris-checker\n```\n\n## Usage\n\nThere are two ways to use this script. The first is to create a file named `ips.txt`:\n\n```bash\n$ echo 127.0.0.1 >> ips.txt\n$ echo 127.0.0.0/29 >> ips.txt\n$ poetry run meris-checker\nIP 127.0.0.1 is safe, whew!\nIP 127.0.0.0 is safe, whew!\nIP 127.0.0.1 is safe, whew!\nIP 127.0.0.2 is safe, whew!\nIP 127.0.0.3 is safe, whew!\nIP 127.0.0.4 is safe, whew!\nIP 127.0.0.5 is safe, whew!\nIP 127.0.0.6 is safe, whew!\nIP 127.0.0.7 is safe, whew!\n```\n\nThe second is to specify the IPs one-at-a-time on the command line:\n\n```bash\n$ poetry run meris-checker 127.0.0.1 127.0.0.0/30\nIP 127.0.0.1 is safe, whew!\nIP 127.0.0.0 is safe, whew!\nIP 127.0.0.1 is safe, whew!\nIP 127.0.0.2 is safe, whew!\nIP 127.0.0.3 is safe, whew!\n```\n\nThis should work with any valid IPv4/IPv6 address or subnet. However, please be aware that it hits the Qrator API for each address in the subnet individually, so you should probably limit your lookups to narrow ranges that you actually own.\n\nThe script is rate-limited to 1 IP query per second, so a /24 will take ~6 minutes to run.\n\n## Contributing\n\nPatches are welcome. Please email don@bloono.com\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Don Spaulding',
    'author_email': 'don@bloono.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hg.sr.ht/~donspaulding/meris-checker/browse',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
