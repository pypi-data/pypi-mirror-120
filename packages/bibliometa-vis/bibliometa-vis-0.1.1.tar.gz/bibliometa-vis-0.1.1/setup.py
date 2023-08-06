# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bibliometa_vis']

package_data = \
{'': ['*']}

install_requires = \
['bibliometa>=0.1.3,<0.2.0',
 'cartopy>=0.20.0,<0.21.0',
 'cython>=0.29.24,<0.30.0',
 'geopandas>=0.9.0,<0.10.0',
 'loguru>=0.5.3,<0.6.0',
 'matplotlib>=3.4.3,<4.0.0',
 'networkx>=2.6.2,<3.0.0',
 'shapely>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'bibliometa-vis',
    'version': '0.1.1',
    'description': 'An extension package for Bibliometa that provides visualization functions',
    'long_description': '# Bibliometa-Vis\n\n[![Documentation Status](https://readthedocs.org/projects/bibliometa-vis/badge/?version=latest)](https://bibliometa-vis.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/bibliometa-vis.svg)](https://badge.fury.io/py/bibliometa-vis)\n\nBibliometa-Vis is a python extension library for [Bibliometa](https://github.com/alueschow/bibliometa) that provides visualization functions.\n\n*Homepage*: https://bibliometa-vis.readthedocs.io\n\n*Repository*: https://github.com/alueschow/bibliometa-vis\n\n*Package*: https://pypi.org/project/bibliometa-vis/\n\n*License*: MIT\n\n-----\n\n## Installation\n* Use pip: ```pip install bibliometa-vis```\n+ **Note**: You may need to install the following packages on your machine in advance (e.g. via `apt-get`) to be able to use Bibliometa:\n  - libproj-dev\n  - proj-data\n  - proj-bin\n  - libgeos-dev\n\n## Development\n* Clone this repository: ```git clone https://github.com/alueschow/bibliometa-vis.git```\n* Run ```poetry install``` to install all necessary dependencies\n* After development, run ```poetry export --without-hashes -f requirements.txt --output requirements.txt``` to create a _requirements.txt_ file with all dependencies. This file is needed to create the documentation on [ReadTheDocs](https://readthedocs.org/).\n* Run ```poetry run sphinx-quickstart``` to initialize the Sphinx documentation\n* Change configuration in ```./docs/source/conf.py```, if needed\n* Run ```poetry run sphinx-apidoc -f -o source ../src/bibliometa_vis``` and then ```poetry run make html``` from within the _docs_ folder to create a local documentation using [Sphinx](https://www.sphinx-doc.org/en/master/).\n\n## Tutorial\nA tutorial that makes use of the Bibliometa and the Bibliometa-Vis packages can be found on GitHub: https://github.com/alueschow/cerl-thesaurus-networks\n',
    'author': 'Andreas Lüschow',
    'author_email': 'lueschow@sub.uni-goettingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bibliometa-vis.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
