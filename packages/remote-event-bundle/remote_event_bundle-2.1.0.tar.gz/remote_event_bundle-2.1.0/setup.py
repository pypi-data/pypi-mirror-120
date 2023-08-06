# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['remote_event_bundle', 'remote_event_bundle.backend']

package_data = \
{'': ['*']}

install_requires = \
['applauncher>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'remote-event-bundle',
    'version': '2.1.0',
    'description': 'Remote events',
    'long_description': None,
    'author': 'Alvaro Garcia',
    'author_email': 'maxpowel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
