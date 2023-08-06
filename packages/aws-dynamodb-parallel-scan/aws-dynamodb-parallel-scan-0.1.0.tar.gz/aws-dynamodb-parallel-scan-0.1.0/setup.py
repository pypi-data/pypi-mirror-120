# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['py']
install_requires = \
['boto3>=1.18.43,<2.0.0']

setup_kwargs = {
    'name': 'aws-dynamodb-parallel-scan',
    'version': '0.1.0',
    'description': 'Amazon DynamoDB Parallel Scan Paginator for boto3.',
    'long_description': None,
    'author': 'Sami Jaktholm',
    'author_email': 'sjakthol@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
