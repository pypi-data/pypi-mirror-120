# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crsf_parser']

package_data = \
{'': ['*']}

install_requires = \
['construct-typing>=0.5,<0.6', 'construct>=2.10,<3.0']

setup_kwargs = {
    'name': 'crsf-parser',
    'version': '0.2.2',
    'description': 'A package to parse and create CRSF (Crossfire) frames, developed primarily to interoperate with ExpressLRS',
    'long_description': '',
    'author': 'Alessio Morale',
    'author_email': 'alessiomorale@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AlessioMorale/crsf_parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
