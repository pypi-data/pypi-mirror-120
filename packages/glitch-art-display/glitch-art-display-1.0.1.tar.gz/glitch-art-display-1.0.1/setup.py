# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glitch_art_display']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0', 'click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['glitch-art-display = glitch_art_display.main:main']}

setup_kwargs = {
    'name': 'glitch-art-display',
    'version': '1.0.1',
    'description': 'Generates .MP4 slideshow with seizure-inducing glitch transitions',
    'long_description': None,
    'author': 'TheTechromancer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
