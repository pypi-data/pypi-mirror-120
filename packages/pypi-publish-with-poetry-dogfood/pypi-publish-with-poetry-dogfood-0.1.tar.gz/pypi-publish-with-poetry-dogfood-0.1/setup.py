# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_publish_with_poetry_dogfood']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypi-publish-with-poetry-dogfood',
    'version': '0.1',
    'description': 'Empty package to test the GitHub Action `coveooss/pypi-publish-with-poetry`',
    'long_description': 'This package is used to validate the functionality of the "coveooss/pypi-publish-with-poetry" GitHub action.\n\nYou can read more about the action [here](https://github.com/coveooss/pypi-publish-with-poetry).\n',
    'author': 'Jonathan Piché',
    'author_email': 'tools@coveo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coveooss/pypi-publish-with-poetry',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
