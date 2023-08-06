# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory',
 'understory.apps.micropub_server',
 'understory.apps.micropub_server.templates']

package_data = \
{'': ['*']}

install_requires = \
['micropub>=0.0.2,<0.0.3', 'understory>=0.0.71,<0.0.72']

setup_kwargs = {
    'name': 'understory-micropub-server',
    'version': '0.0.2',
    'description': 'A Micropub server for the Understory framework.',
    'long_description': '# understory-micropub-server\n\nA [Micropub][0] client for the [Understory][1] framework.\n\n[0]: https://micropub.spec.indieweb.org\n[1]: https://github.com/canopy/understory\n',
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
