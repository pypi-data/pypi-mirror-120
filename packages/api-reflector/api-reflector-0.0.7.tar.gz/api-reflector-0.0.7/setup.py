# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api_reflector']

package_data = \
{'': ['*'], 'api_reflector': ['templates/admin/*']}

modules = \
['settings']
install_requires = \
['Flask-Admin>=1.5.8,<2.0.0',
 'Flask-Dance>=5.0.0,<6.0.0',
 'Flask-SQLAlchemy>=2.5.1,<3.0.0',
 'Flask>=2.0.1,<3.0.0',
 'Jinja2>=3.0.1,<4.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'api-reflector',
    'version': '0.0.7',
    'description': 'A configurable API mocking service',
    'long_description': 'None',
    'author': 'Chris Latham',
    'author_email': 'cl@bink.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
