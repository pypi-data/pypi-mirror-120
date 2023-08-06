# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api_auth', 'mifiel', 'mifiel.api_auth']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.0']

setup_kwargs = {
    'name': 'mifiel',
    'version': '0.0.12',
    'description': 'Python API Client library for mifiel.com',
    'long_description': "# Mifiel Python Library\n\n[![Coverage Status][coveralls-image]][coveralls-url]\n[![Build Status][travis-image]][travis-url]\n[![PyPI version][pypi-image]][pypi-url]\n\nPython library for [Mifiel](https://www.mifiel.com) API.\nPlease read our [documentation](http://docs.mifiel.com) for instructions on how to start using the API.\n\n## Installation\n\n```bash\npip install mifiel\n```\n\n## Usage\n\nFor your convenience Mifiel offers a Sandbox environment where you can confidently test your code.\n\nTo start using the API in the Sandbox environment you need to first create an account at [sandbox.mifiel.com](https://sandbox.mifiel.com).\n\nOnce you have an account you will need an APP_ID and an APP_SECRET which you can generate in [sandbox.mifiel.com/access_tokens](https://sandbox.mifiel.com/access_tokens).\n\n### Document methods:\n\nFor now, the only methods available are **find** and **create**. Contributions are greatly appreciated.\n\n- Find:\n\n```python\nfrom mifiel import Document, Client\nclient = Client(app_id='APP_ID', secret_key='APP_SECRET')\n\ndoc = Document.find(client, 'id')\ndocument.original_hash\ndocument.file\ndocument.file_signed\n# ...\n```\n\n- Create:\n\n```python\nfrom mifiel import Document, Client\nclient = Client(app_id='APP_ID', secret_key='APP_SECRET')\n\nsignatories = [\n  { \n    'name': 'Signer 1', \n    'email': 'signer1@email.com', \n    'tax_id': 'AAA010101AAA' \n  },\n  { \n    'name': 'Signer 2', \n    'email': \n    'signer2@email.com', \n    'tax_id': 'AAA010102AAA'\n  }\n]\n# Providde the SHA256 hash of the file you want to sign.\ndoc = Document.create(client, signatories, dhash='some-sha256-hash')\n# Or just send the file and we'll take care of everything.\n# We will store the file for you. \ndoc = Document.create(client, signatories, file='test/fixtures/example.pdf')\n\ndoc.id # -> '7500e528-ac6f-4ad3-9afd-74487c11576a'\ndoc.id # -> '7500e528-ac6f-4ad3-9afd-74487c11576a'\n```\n\n- Save Document related files\n\n```python\nfrom mifiel import Document, Client\nclient = Client(app_id='APP_ID', secret_key='APP_SECRET')\n\ndoc = Document.find(client, 'id')\n# save the original file\ndoc.save_file('path/to/save/file.pdf')\n# save the signed file (original file + signatures page)\ndoc.save_file_signed('path/to/save/file-signed.pdf')\n# save the signed xml file\ndoc.save_xml('path/to/save/xml.xml')\n```\n\n## Development\n\n### Install dependencies\n\n```bash\npip install -r requirements.txt\n```\n\n## Test\n\nJust clone the repo, install dependencies as you would in development and run `nose2` or `python setup.py test`\n\n## Contributing\n\n1. Fork it ( https://github.com/Mifiel/python-api-client/fork )\n2. Create your feature branch (`git checkout -b my-new-feature`)\n3. Commit your changes (`git commit -am 'Add some feature'`)\n4. Push to the branch (`git push origin my-new-feature`)\n5. Create a new Pull Request\n\n[coveralls-image]: https://coveralls.io/repos/github/Mifiel/python-api-client/badge.svg?branch=master\n[coveralls-url]: https://coveralls.io/github/Mifiel/python-api-client?branch=master\n\n[travis-image]: https://travis-ci.org/Mifiel/python-api-client.svg?branch=master\n[travis-url]: https://travis-ci.org/Mifiel/python-api-client\n\n[pypi-image]: https://badge.fury.io/py/mifiel.svg\n[pypi-url]: https://badge.fury.io/py/mifiel\n",
    'author': 'Genaro Madrid',
    'author_email': 'genmadrid@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/mifiel/python-api-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
