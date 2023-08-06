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
    'version': '0.1.1',
    'description': 'A command-line utility for pulling code blocks out of markdown files.',
    'long_description': "A command-line utility for pulling code blocks out of markdown files.\n\n```sh\n$ pip install mkcodes\n\n# For traditional markdown code-block support.\n$ pip install mkcodes[markdown]\n\n$ mkcodes --help\nUsage: mkcodes [OPTIONS] INPUTS...\n\nOptions:\n  --output TEXT\n  --github / --markdown  Github-flavored fence blocks or pure markdown.\n  --safe / --unsafe      Allow code blocks without language hints.\n  --package-python       Add __init__.py files to python dirs for test\n                         discovery\n  --default-lang TEXT    Assumed language for code blocks without language\n                         hints.\n  --help                 Show this message and exit.\n```\n\nWhy would I want such a thing?\n------------------------------\n\nMy purpose is testing.\n\nYou can easily enough doctest a markdown file with `python -m doctest myfile.md`, but I don't like typing or looking at a whole bunch of `>>>` and `...`'s. Also there's no way that I know of to run linters against such code blocks.\n\nInstead, I include (pytest) functional tests in my codeblocks, extract the code blocks with this script, and then run my test runner and linters against the output files.\n\nRunning Tests\n-------------\n\n```sh\n./test\n```\n",
    'author': 'ryneeverett',
    'author_email': 'ryneeverett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ryneeverett/mkcodes',
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
