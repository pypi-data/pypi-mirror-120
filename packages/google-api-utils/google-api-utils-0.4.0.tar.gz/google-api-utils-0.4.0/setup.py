# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_api_utils']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client==2.4.0', 'oauth2client==4.1.3', 'pandas==1.3.3']

setup_kwargs = {
    'name': 'google-api-utils',
    'version': '0.4.0',
    'description': 'Google API services for python',
    'long_description': '# finance-google-utils\n\nFinance repository intended to store Classes and Functions related to Google Services such as Drive, Sheets, Docs...',
    'author': 'LucasCiziks',
    'author_email': 'lucas.ciziks@loft.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/loft-br/finance-google-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
