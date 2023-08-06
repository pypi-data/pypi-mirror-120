# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['456789999999test',
 '456789999999test.grader',
 '456789999999test.json',
 '456789999999test.ninja_robot',
 '456789999999test.pdf']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2', 'fpdf']

setup_kwargs = {
    'name': '456789999999test',
    'version': '1.0.0',
    'description': 'Jupyter Notebook Image Classification assessment tool',
    'long_description': '',
    'author': 'test',
    'author_email': 'test@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/3421321321/test',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*',
}


setup(**setup_kwargs)
