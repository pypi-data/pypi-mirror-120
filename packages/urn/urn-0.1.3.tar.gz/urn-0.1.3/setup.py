# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['urn']
setup_kwargs = {
    'name': 'urn',
    'version': '0.1.3',
    'description': 'Urn is a micro RPC framework',
    'long_description': None,
    'author': 'Imtiaz Mangerah',
    'author_email': 'Imtiaz_Mangerah@a2d24.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
