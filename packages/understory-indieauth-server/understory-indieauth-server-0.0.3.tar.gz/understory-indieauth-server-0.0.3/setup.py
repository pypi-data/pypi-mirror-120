# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory',
 'understory.apps.indieauth_server',
 'understory.apps.indieauth_server.templates']

package_data = \
{'': ['*']}

install_requires = \
['indieauth>=0.0.4,<0.0.5', 'understory>=0.0.71,<0.0.72']

setup_kwargs = {
    'name': 'understory-indieauth-server',
    'version': '0.0.3',
    'description': 'An IndieAuth server for the Understory framework.',
    'long_description': '# understory-indieauth-server\n\nAn [IndieAuth][0] server for the [Understory][1] framework.\n\n[0]: https://indieauth.spec.indieweb.org\n[1]: https://github.com/canopy/understory\n',
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
