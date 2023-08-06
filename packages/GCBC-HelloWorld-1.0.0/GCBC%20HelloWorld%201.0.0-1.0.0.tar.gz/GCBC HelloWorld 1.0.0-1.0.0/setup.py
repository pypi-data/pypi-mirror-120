#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "GCBC HelloWorld 1.0.0"
DESCRIPTION = "An example of packaging code"
URL = "https://github.com/goodcodebadcode/pypi-helloworld"
EMAIL = "david@goodcodebadcode.com"
AUTHOR = "David Ritchie"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "1.0.0"

# What packages are required for this module to be executed?
_INSTALL_REQUIRES = [
    "click",
    "requests",
    "PyGithub==1.53.0"
]

# The directory containing this file
here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

# This call to setup() does all the work
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=_INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "pypi-helloworold=helloworld.helloworld:hello_world",
        ]
    },
)