# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymacro']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-pymacro',
    'version': '0.1.0',
    'description': 'A python library that can be used to have macros inside python functions through decorators.',
    'long_description': '# PyMacro\n\nWelcome to *pymacro*, a python library that you can use to have MACROS inside your python functions.\nIt uses a decorator to find and replace macros inside of comments with valid python code. It can \nbe used in the following manner.\n\n```py\nfrom pymacro import macro\n\n@macro\ndef func_with_macro():\n    # DEFINE x 10\n    print(x)\n```\n\nThe DSL inside the comments is turned into valid python code.',
    'author': 'AbooMinister25',
    'author_email': 'aboominister@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AbooMinister25/pymacro',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
