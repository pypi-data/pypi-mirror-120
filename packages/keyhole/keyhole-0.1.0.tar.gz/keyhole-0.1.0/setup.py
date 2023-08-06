# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keyhole', 'keyhole.mosaick', 'keyhole.register']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20,<2.0',
 'pyvips>=2.1.15,<3.0.0',
 'scikit-image>=0.18,<0.19',
 'scipy>=1.7,<2.0',
 'tqdm>=4.62.0,<5.0.0']

entry_points = \
{'console_scripts': ['keyhole = keyhole.cli:main']}

setup_kwargs = {
    'name': 'keyhole',
    'version': '0.1.0',
    'description': 'Work with declassified keyhole satellite images.',
    'long_description': None,
    'author': 'Seth Warn',
    'author_email': 'swarn@uark.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
