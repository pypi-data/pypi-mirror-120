# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testcases', 'testcases.TestInputs']

package_data = \
{'': ['*']}

install_requires = \
['insight-engine-schema-python>=0.1.7,<0.2.0',
 'rialtic-data-dev-py>=0.11.6,<0.12.0']

setup_kwargs = {
    'name': 'policy-scaffolding-python',
    'version': '0.2.11',
    'description': 'Scaffolding project to support Rialtic Insight Engine development in Python.',
    'long_description': "# Engine development scaffolding (Python)\n\nScaffolding project to support engine development in Python.\n\nThis subproject provides a Python library to facilitate test-driven development\nof engines.\n\n## Test cases generation\n\nIn order to develop an engine and to be able to check if the engine\nworks as expected, a test-driven development approach proved to be\nvaluable. Test cases might be very well understood by both the content\ndesigner and engine developer.\n\nThis project contains DSL (domain-specific language) written in Python \nto help generate test cases. \n\nBefore starting using Python it's recommended to create a virtual environment \nto avoid conflicts.\n\n```sh\npython3 -m venv .venv-local\n```\nThis command will create a new virtual environment in the folder `.venv-local`.\nThen in a new terminal it needs to be activated:\n\n```sh\nsource .venv-local/bin/activate\n```\n\nTo generate test cases for ambulance:\n\n```sh\npython ambulance.py\n```\n",
    'author': 'Rialtic',
    'author_email': 'engines.data@rialtic.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rialtic.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
