# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acnutils']

package_data = \
{'': ['*']}

install_requires = \
['pywikibot>=6.6.1,<7.0.0', 'toolforge>=5.0.0,<6.0.0']

setup_kwargs = {
    'name': 'acnutils',
    'version': '0.1.0',
    'description': "Various utilities used in AntiCompositeNumber's bots",
    'long_description': "acnutils\n========\n.. image:: https://img.shields.io/github/workflow/status/AntiCompositeNumber/AntiCompositeBot/Python%20application\n    :alt: GitHub Workflow Status\n.. image:: https://coveralls.io/repos/github/AntiCompositeNumber/acnutils/badge.svg?branch=master\n    :target: https://coveralls.io/github/AntiCompositeNumber/acnutils?branch=master\n    :alt: Coverage status\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :alt: Code style: black\n    :target: https://github.com/psf/black\n\n\nA collection of various scripts used by AntiCompositeNumber's bots.\n\nFeel free to use this if you find it useful, however, no guarentees of stability are made.\nPull requests are welcome, but may be declined if they would not be useful for my bots or tools.\n\nPoetry is used for dependency management and package building.\n",
    'author': 'AntiCompositeNumber',
    'author_email': 'anticompositenumber+pypi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AntiCompositeNumber/acnutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
