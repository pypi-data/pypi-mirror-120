# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spyrmsd', 'spyrmsd.graphs', 'spyrmsd.optional']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2', 'numpy>=1.19.2,<2.0.0', 'scipy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'spyrmsd',
    'version': '0.5.1',
    'description': 'symmetry-corrected RMSD in Python',
    'long_description': None,
    'author': 'Rocco Meli',
    'author_email': 'rocco.meli@biodtp.ox.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
