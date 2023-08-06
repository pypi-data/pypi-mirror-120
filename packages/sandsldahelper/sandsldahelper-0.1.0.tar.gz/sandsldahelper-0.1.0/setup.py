# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sandsldahelper']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.9.2,<4.0.0',
 'isort>=5.9.3,<6.0.0',
 'msgpack>=1.0.2,<2.0.0',
 'nltk>=3.6.2,<4.0.0',
 'numpy>=1.21.2,<2.0.0',
 'openpyxl>=3.0.8,<4.0.0',
 'pandas>=1.3.3,<2.0.0',
 'pretty-errors>=1.2.24,<2.0.0',
 'pyLDAvis>=3.3.1,<4.0.0',
 'pyarrow>=5.0.0,<6.0.0',
 'sandspythonfunctions>=0.1.0,<0.2.0',
 'spacy>=3.1.2,<4.0.0',
 'tomotopy>=0.12.2,<0.13.0',
 'tqdm>=4.62.2,<5.0.0',
 'vaex>=4.5.0,<5.0.0',
 'wheel>=0.37.0,<0.38.0',
 'zstandard>=0.15.2,<0.16.0']

setup_kwargs = {
    'name': 'sandsldahelper',
    'version': '0.1.0',
    'description': 'This python package is meant to make creating, testing and creating useful output files for LDA topic modeling much easier. It uses Tomotopy for the topic modeling.',
    'long_description': None,
    'author': 'Levi Sands',
    'author_email': 'ldsands@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
