# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nmh', 'nmh.git']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'nmh',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Huy tran',
    'author_email': 'huy.td183768@sis.hust.edu.vn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
