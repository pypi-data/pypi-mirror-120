# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['user_email', 'user_email.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.7,<4.0.0']

setup_kwargs = {
    'name': 'django-user-email',
    'version': '0.2.0',
    'description': 'Custom, simple Django User model with email as username',
    'long_description': '<h1 align="center">\n  django-user-email\n</h1>\n\n<p align="center">\n  <a href="#installation">Installation</a> •\n  <a href="#contributing">Contributing</a> •\n  <a href="#license">License</a>\n</p>\n\n<p align="center">Custom, simple Django User model with email as username</p>\n\n## Installation\n\n1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install numiner.\n\n```bash\n$ pip install django-user-email\n```\n\n2. Register the app to your settings\n\n```python\nINSTALLED_APPS = (\n    ...\n    \'user_email\',\n)\n```\n\n3. Since it\'s a custom User model Django needs to know the path of the model\n\n```bash\nAUTH_USER_MODEL = \'user_email.User\'\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT License](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Khasbilegt.TS',
    'author_email': 'khasbilegt.ts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khasbilegt/django-user-email',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
