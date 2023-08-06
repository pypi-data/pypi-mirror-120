# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drive_utils']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client==2.4.0', 'oauth2client==4.1.3', 'pandas==1.3.3']

setup_kwargs = {
    'name': 'drive-utils',
    'version': '1.0.0',
    'description': 'Useful functions of Google Drive API for python',
    'long_description': '# finance-drive-utils\n\nFinance Package intended to store Classes and Functions related to Google Services such as Drive, Sheets, Docs...',
    'author': 'LucasCiziks',
    'author_email': 'lucas.ciziks@loft.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/loft-br/finance-drive-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
