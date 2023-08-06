# Bibliometa-Vis

[![Documentation Status](https://readthedocs.org/projects/bibliometa-vis/badge/?version=latest)](https://bibliometa-vis.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/bibliometa-vis.svg)](https://badge.fury.io/py/bibliometa-vis)

Bibliometa-Vis is a python extension library for [Bibliometa](https://github.com/alueschow/bibliometa) that provides visualization functions.

*Homepage*: https://bibliometa-vis.readthedocs.io

*Repository*: https://github.com/alueschow/bibliometa-vis

*Package*: https://pypi.org/project/bibliometa-vis/

*License*: MIT

-----

## Installation
* Use pip: ```pip install bibliometa-vis```
+ **Note**: You may need to install the following packages on your machine in advance (e.g. via `apt-get`) to be able to use Bibliometa:
  - libproj-dev
  - proj-data
  - proj-bin
  - libgeos-dev

## Development
* Clone this repository: ```git clone https://github.com/alueschow/bibliometa-vis.git```
* Run ```poetry install``` to install all necessary dependencies
* After development, run ```poetry export --without-hashes -f requirements.txt --output requirements.txt``` to create a _requirements.txt_ file with all dependencies. This file is needed to create the documentation on [ReadTheDocs](https://readthedocs.org/).
* Run ```poetry run sphinx-quickstart``` to initialize the Sphinx documentation
* Change configuration in ```./docs/source/conf.py```, if needed
* Run ```poetry run sphinx-apidoc -f -o source ../src/bibliometa_vis``` and then ```poetry run make html``` from within the _docs_ folder to create a local documentation using [Sphinx](https://www.sphinx-doc.org/en/master/).

## Tutorial
A tutorial that makes use of the Bibliometa and the Bibliometa-Vis packages can be found on GitHub: https://github.com/alueschow/cerl-thesaurus-networks
