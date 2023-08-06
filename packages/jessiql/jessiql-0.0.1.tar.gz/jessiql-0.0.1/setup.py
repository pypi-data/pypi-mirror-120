# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jessiql',
 'jessiql.engine',
 'jessiql.features',
 'jessiql.features.cursor',
 'jessiql.features.cursor.cursors',
 'jessiql.integration',
 'jessiql.integration.fastapi',
 'jessiql.integration.graphql',
 'jessiql.integration.graphql.query_field',
 'jessiql.operations',
 'jessiql.query_object',
 'jessiql.sainfo',
 'jessiql.sautil',
 'jessiql.testing',
 'jessiql.util']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[mypy]']

setup_kwargs = {
    'name': 'jessiql',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Mark Vartanyan',
    'author_email': 'kolypto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kolypto/py-jessiql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
