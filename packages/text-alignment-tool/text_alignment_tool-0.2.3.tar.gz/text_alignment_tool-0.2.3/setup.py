# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['text_alignment',
 'text_alignment.alignment_algorithms',
 'text_alignment.alignment_tool',
 'text_alignment.find_wordlist_for_alignment',
 'text_alignment.shared_classes',
 'text_alignment.text_loaders',
 'text_alignment.text_transformers']

package_data = \
{'': ['*']}

install_requires = \
['bidict>=0.21.3,<0.22.0',
 'colored>=1.4.2,<2.0.0',
 'cursive-re>=0.0.4,<0.0.5',
 'dotmap>=1.3.24,<2.0.0',
 'edlib>=1.3.9,<2.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'lxml>=4.6.3,<5.0.0',
 'numpy>=1.17,<2.0',
 'pandas>=1.3.3,<2.0.0',
 'swalign>=0.3.6,<0.4.0',
 'terminaltables>=3.1.0,<4.0.0',
 'tqdm>=4.62.2,<5.0.0',
 'typing>=3.6.0,<4.0.0']

setup_kwargs = {
    'name': 'text-alignment-tool',
    'version': '0.2.3',
    'description': 'A pipeline tool for performing customized text alignment procedures',
    'long_description': None,
    'author': 'Bronson Brown-deVost',
    'author_email': 'bronsonbdevost@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
