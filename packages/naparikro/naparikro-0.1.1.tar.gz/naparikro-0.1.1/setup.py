# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['naparikro']

package_data = \
{'': ['*']}

install_requires = \
['arkitekt>=0.1.11,<0.2.0', 'mikro>=0.1.7,<0.2.0']

entry_points = \
{'console_scripts': ['mikroj = naparikro.run:main']}

setup_kwargs = {
    'name': 'naparikro',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
