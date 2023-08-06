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
    'version': '0.1.2',
    'description': 'Automatically build Django models from an Excel file',
    'long_description': '\nHave an Excel tool that you\'d like to quickly convert to a Django project? `django-from-excel` is the answer.\n\n## Features\n\n1. Generates models.py file:\n   1. Generate a Django model for each table/sheet in your Excel file\n   2. Create appropriate field types for each of your table columns, with Pythonic naming\n   3. TODO: Detect nullable columns\n   4. TODO: Identify columns that should be foreign keys, and create corresponding models with choice fields\n2. Generates admin.py file:\n   1. Registers all models created in Step 1\n3. Optionally creates migration files and migrates the schema\n4. Optionally generates fixtures and loads data into your database\n\nWith a single command, you will be able to explore your data in the Django admin.\n\n---\n\n# Usage\n\nThe following instructions assume you already have a Django project and at least one app set up.\n\n## Installation\n\n``` sh\npip install django-from-excel\n```\n\n## Setup\n\nLocate the Excel file that has the data you want to build models from. It should have a table of data, like this:\n\n![Example Excel file](static/img/fleet.xlsx.png)\n\nCopy this file to a location in the project that is easy to reference. The simplest approach is to place it in the same directory as `manage.py`, as that is where you\'ll need to run the command from.\n\nBefore continuing, make sure you have created an app, and that it is registered in `settings.INSTALLED_APPS`.\n\nAdd `django_from_excel` to `settings.INSTALLED_APPS`.\n\nAt this point, also confirm your database settings.\n\n## Run\n\nExample:\n\n``` sh\nmanage.py buildfrom fleet.xlsx app --overwrite --migrate --loaddata\n  ```\n\nThe following options are available for the `buildfrom` command:\n\n**filepath:**\n\nRequired. The filepath or path/to/filepath for the Excel file to generate models from.\n\n**app:**\n\nRequired. The app to generate `models.py` and `admin.py` files in. Must already exist, and must be listed in `settings.INSTALLED_APPS`.\n\n**--overwrite:**\n\nWill overwrite existing `admin.py` and `models.py` files in the target app; otherwise, a unique hex string will be appended to the file names, such as `models_120f77f8.py`.\n\nWARNING: If you have existing models and specify `--overwrite`, they will be lost forever!\n\n**--migrate:**\n\nAfter generating the models, this will automatically run `manage.py makemigrations` and `manage.py migrate`.\n\n**--loaddata:**\n\nOnce migrations are complete, this will generate a `convertedmodel.json` file in `<app>/fixtures`, and will then call the `manage.py loaddata convertedmodel.json <app>` command.\nMust be used in conjunction with `--migrate`.\n\n``` json\n[\n    {\n        "model": "app.convertedmodel",\n        "pk": 1,\n        "fields": {\n            "vin": "JN8AF5MV9BT005581",\n            "year": 2021,\n            "make": "Chevrolet",\n            "model": "Silverado 1500",\n            "mileage": 25000,\n            "color": "White",\n            "engine_size_liters": 6.2,\n            "fuel_type": "gasoline",\n            "avg_mpg": 24.5394832,\n            "is_leased": true\n        }\n    }\n]\n```\n\n## Inspect\n\nView the `models.py` and `admin.py` files that were generated.\n\nIf you chose the `--migrate` option:\n\nLog in to the [Django admin](http://localhost:8000/admin/). Your converted model(s) should be listed there.\n\n![Converted models in Django admin](static/img/django-admin.png)\n\nIf you specified `--loaddata`:\n\nOpen the model, and you should have a record for each row in the original Excel file.\n\n![Example record in converted model](static/img/converted-model.png)\n\n## Eject\n\nOnce you are satisfied with the results, you can remove `django_from_excel` from `settings.INSTALLED_APPS` and uninstall `django-from-excel` and any other dependencies you don\'t need for your project.\n\nTODO: Create an eject command to handle this automatically.\n\n## Build Your Dream App\n\nThis is only intended to create a starting point. You\'ll want to inspect the models to make sure the field types are correct, you\'ll likely need to add some nullable fields or unique constraints, and you may need to spin some fields off into their own tables, with foreign keys linking back.\n\n---\n\n# Common Errors\n\n## Unknown command: \'buildfrom\'\n\nSolution: Add `django_from_excel` to `settings.INSTALLED_APPS`.',
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
