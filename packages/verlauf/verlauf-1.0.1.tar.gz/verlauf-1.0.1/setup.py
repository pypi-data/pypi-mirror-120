# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['verlauf']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['verlauf = verlauf.__main__:main']}

setup_kwargs = {
    'name': 'verlauf',
    'version': '1.0.1',
    'description': 'Verlauf - The Terminal Color Gradient Generator',
    'long_description': "Verlauf - The Terminal Color Gradient Generator\n===============================================\n\n.. image:: ./screenshot/screen.jpg\n\nInstallation\n------------\n\nTo install ``verlauf``, simply run\n\n::\n\n    pip install verlauf\n\nUsage\n-----\n\n::\n\n    verlauf [start] [end] [steps]\n\n\nExamples\n--------\n\n::\n\n    $ verlauf --help\n    Usage: gradients.py [OPTIONS] START END [STEPS]\n\n      Generates a gradient from START to END STEPS long (ends inclusive)\n\n    Options:\n      --help  Show this message and exit.\n    $ verlauf f00 00f           # This produces 5 colors between #ff0000 and #0000ff\n    $ verlauf '#0abc0d' abcdef  # '#' in color names are optional\n    $ verlauf 0abc0d abcdef 7   # This will produce 7 colors in between\n\n",
    'author': 'Ceda EI',
    'author_email': 'ceda_ei@webionite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ceda_ei/verlauf.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
