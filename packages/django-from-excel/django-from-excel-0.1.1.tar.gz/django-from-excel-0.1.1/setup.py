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
    'version': '0.1.1',
    'description': 'Automatically builds Django models from an Excel file',
    'long_description': "# django-from-excel\nAutomatically builds Django models from an Excel file\n\n## Getting Started\n\nThe following instructions assume you already have a Django project and at least one app set up.\n\n### Installation\n\n``` sh\npip install django-from-excel\n```\n\n### Setup\n\nCopy the Excel file you want to convert to a location in the project that is easy to reference. The simplest approach is to place it in the same directory as `manage.py`, as that is where you'll need to run the command from.\n\nBefore continuing, make sure you have created an app, and that it is registered in `settings.INSTALLED_APPS`.\n\nAdd `django_from_excel` to `settings.INSTALLED_APPS`.\n\nAt this point, also confirm your database settings.\n\n### Run\n\nExample:\n\n``` sh\nmanage.py buildfrom tracker.xlsx app --overwrite --migrate --loaddata\n  ```\n\nThe following options are available for the `buildfrom` command:\n\n**filename:**\n\nRequired. The filename or path/to/filename for the Excel file to generate models from.\n\n**app:**\n\nRequired. The app to generate `models.py` and `admin.py` files in. Must already exist, and must be listed in `settings.INSTALLED_APPS`.\n\n**--overwrite:**\n\nWill overwrite existing `admin.py` and `models.py` files in the target app; otherwise, a unique hex string will be appended to the filenames, such as `models_120f77f8.py`.\n\nWARNING: If you have existing models and specify `--overwrite`, they will be lost forever!\n\n**--migrate:**\n\nAfter generating the models, this will automatically run `manage.py makemigrations` and `manage.py migrate`.\n\n**--loaddata:**\n\nOnce migrations are complete, this will generate a `convertedmodel.json` file in `<app>/fixtures`, and will then call the `manage.py loaddata convertedmodel.json <app>` command.\nMust be used in conjunction with `--migrate`.\n\n### Inspect\n\nView the `models.py` and `admin.py` files that were generated.\n\nIf you chose the `--migrate` option:\n\nLog in to the [Django admin](http://localhost:8000/admin/). Your converted model(s) should be listed there.\n\nIf you specified `--loaddata`:\n\nOpen the model, and you should have a record for each row in the original Excel file.\n\n### Build Your Dream App\n\nThis is only intended to create a starting point. You'll want to inspect the models to make sure the field types are correct, you'll likely need to add some nullable fields or unique constraints, and you may need to spin some fields off into their own tables, with foreign keys linking back. But, hopefully `django-from-excel` saved you time by quickly creating some Django models for you.\n\n### Eject\n\nOnce you are satisfied with the results, you can remove `django_from_excel` from `settings.INSTALLED_APPS` and uninstall `django-from-excel` and any other dependencies you don't need for your project.\n\n---\n\n## TODO's\n\n1. Detect nullable data by columns with blank cells, while maintaining ability to detect column's data type\n2. Detect duplicate data that should be in a foreign table, and create corresponding ForeignKey field\n3. Create an eject command\n\n\n\n\n\n",
    'author': 'John Macy',
    'author_email': 'johncmacy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/johncmacy/django-from-excel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
