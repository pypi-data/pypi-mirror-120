# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_project', 'fastapi_project.components']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['fastapi-cli = fastapi_project.manage:app']}

setup_kwargs = {
    'name': 'fastapi-project',
    'version': '0.1.0',
    'description': 'Create FastAPI Application using this CLI',
    'long_description': '# FastAPI CLI\nCreate FastAPI Application Set Up using this CLI\n## Author : Gian Carlo L. Garcia\n\nVersion : v.0.1.0\n\n### How to use ?\n\n` pip install fastapi-project`\n\n` fastapi_project create-app  <app-name>`',
    'author': 'Gian Carlo Llanes Garcia',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
