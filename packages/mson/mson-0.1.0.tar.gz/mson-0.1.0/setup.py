# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mson']

package_data = \
{'': ['*']}

install_requires = \
['lark>=0.11.3,<0.12.0', 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'mson',
    'version': '0.1.0',
    'description': 'MSON serializer/de-serializer',
    'long_description': None,
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
