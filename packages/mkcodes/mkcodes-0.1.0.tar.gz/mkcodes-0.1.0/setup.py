# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mkcodes']
install_requires = \
['click']

extras_require = \
{'markdown': ['Markdown']}

entry_points = \
{'console_scripts': ['mkcodes = mkcodes:main']}

setup_kwargs = {
    'name': 'mkcodes',
    'version': '0.1.0',
    'description': 'A command-line utility for pulling code blocks out of markdown files.',
    'long_description': None,
    'author': 'ryneeverett',
    'author_email': 'ryneeverett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
