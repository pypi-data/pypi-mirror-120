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
    'version': '1.0.0',
    'description': 'A script which checks the qrator database to see if any of your IPs is listed as part of the Meris botnet.',
    'long_description': None,
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
