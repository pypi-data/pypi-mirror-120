# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hodgepodge',
 'hodgepodge.cli',
 'hodgepodge.cli.command_groups',
 'hodgepodge.objects',
 'hodgepodge.objects.host',
 'hodgepodge.toolkits',
 'hodgepodge.toolkits.host',
 'hodgepodge.toolkits.host.file_search']

package_data = \
{'': ['*']}

install_requires = \
['DAWG>=0.8.0,<0.9.0',
 'arrow>=1.0.3,<1.1.0',
 'click>=7.0,<8.0',
 'dacite>=1.6.0,<1.7.0',
 'python-dateutil>=2.7.3,<2.8.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.22.0,<2.23.0',
 'setuptools>=45.2.0,<45.3.0',
 'stix2>=3.0.0,<3.1.0',
 'taxii2-client>=2.3.0,<3.0.0',
 'urllib3>=1.25.8,<1.26.0']

entry_points = \
{'console_scripts': ['hodgepodge = hodgepodge.cli:cli']}

setup_kwargs = {
    'name': 'hodgepodge',
    'version': '0.2.0',
    'description': '',
    'long_description': "# hodgepodge\n\n> _A **hodgepodge** of hopefully helpful helper code_\n\n![These are a few of my favourite functions](https://raw.githubusercontent.com/whitfieldsdad/images/main/a-few-of-my-favourite-things.jpg)\n\n## Features\n\n- Search for files and directories;\n- Hash files;\n- Pack files into ZIP archives;\n- Perform pattern matching using regular expressions or UNIX-style glob patterns;\n- Compress and decompress objects;\n- Parse dates and times;\n- Read STIX 2.0 objects from local files, directories, or TAXII servers 🚖🚦;\n- Make the outputs from your tools more human-readable (e.g., by pretty-printing dates, file sizes, timestamps, and durations, joining lists with an Oxford comma); and\n- ✨ _Way_, __*way*__, __way__ more ✨.\n\nSupported hash algorithms:\n- MD5\n- SHA-1\n- SHA-256\n- SHA-512\n\nSupported archive formats:\n- ZIP\n\nSupported compression algorithms:\n- GZIP\n\n## Installation\n\nTo install using `pip`:\n\n```shell\n$ pip install hodgepodge\n```\n\nTo install from source using `poetry`\n\n```shell\n$ git clone git@github.com:whitfieldsdad/hodgepodge.git\n$ make install\n```\n\nTo install from source using `setup.py`:\n\n```shell\n$ git clone git@github.com:whitfieldsdad/hodgepodge.git\n$ python3 setup.py install\n```\n\n## Install or update build dependencies\n\nThe following Makefile goal can be used to install or update build dependencies as needed:\n\n```shell\n$ make update\n```\n\n## Tests\n\nYou can run the unit tests and measure code coverage at the same time as follows:\n\n```shell\n$ make test\nmake test\npoetry run coverage run -m pytest\n================================= test session starts =================================\nplatform linux -- Python 3.8.10, pytest-5.4.3, py-1.10.0, pluggy-0.13.1\nrootdir: /home/fishet/src/hodgepodge\ncollected 59 items\n\ntests/test_classes.py ...                                                       [  5%]\ntests/test_compression.py ..                                                    [  8%]\ntests/test_files.py ............                                                [ 28%]\ntests/test_hashing.py ..                                                        [ 32%]\ntests/test_patterns.py .....                                                    [ 40%]\ntests/test_platforms.py .                                                       [ 42%]\ntests/test_stix2.py ......                                                      [ 52%]\ntests/test_time.py ...                                                          [ 57%]\ntests/test_type.py ......                                                       [ 67%]\ntests/test_uuid.py .                                                            [ 69%]\ntests/test_ux.py ........                                                       [ 83%]\ntests/toolkits/host/file/test_search.py ..........                              [100%]\n\n================================= 59 passed in 5.12s ==================================\n````\n\nA code coverage report will automatically be written to: `htmlcov/index.html` whenever you run `tox`.\n\nOn Linux systems, you can use `xdg-open` to open the file using the system's default web browser:\n\n```shell\n$ xdg-open htmlcov/index.html\n```\n",
    'author': 'Tyler Fisher',
    'author_email': 'tylerfisher@tylerfisher.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4',
}


setup(**setup_kwargs)
