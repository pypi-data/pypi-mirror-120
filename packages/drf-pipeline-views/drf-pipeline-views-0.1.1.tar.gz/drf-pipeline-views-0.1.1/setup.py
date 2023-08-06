# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipeline_views']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.6,<4.0.0', 'djangorestframework>=3.12.4,<4.0.0']

setup_kwargs = {
    'name': 'drf-pipeline-views',
    'version': '0.1.1',
    'description': 'Django REST framework views using the pipeline pattern.',
    'long_description': None,
    'author': 'Matti Lamppu',
    'author_email': 'lamppu.matti.akseli@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
