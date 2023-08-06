# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_from_excel',
 'django_from_excel.management',
 'django_from_excel.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.7,<4.0.0', 'openpyxl>=3.0.8,<4.0.0', 'pandas>=1.3.3,<2.0.0']

setup_kwargs = {
    'name': 'django-from-excel',
    'version': '0.1.0',
    'description': 'Automatically builds Django models from an Excel file',
    'long_description': None,
    'author': 'John Macy',
    'author_email': '36553266+johncmacy@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
