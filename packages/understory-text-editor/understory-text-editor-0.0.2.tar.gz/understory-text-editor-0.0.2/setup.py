# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory',
 'understory.apps.text_editor',
 'understory.apps.text_editor.templates']

package_data = \
{'': ['*']}

install_requires = \
['micropub>=0.0.2,<0.0.3', 'understory>=0.0.71,<0.0.72']

setup_kwargs = {
    'name': 'understory-text-editor',
    'version': '0.0.2',
    'description': 'A text editor Micropub client for the Understory framework.',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'self@angelogladding.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
