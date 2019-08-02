#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:

import os
import re
import sys
from distutils.core import setup, run_setup

version = '0.0.1'

install_requires = [
    'ply',
]

small_description = 'A set of tools/lib to extract/parse things from Hearts of Iron 4 game files'

try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
    description = f.read()
    f.close()
except IOError:
    description = small_description

try:
    license = open('LICENSE').read()
except IOError:
    license = 'MIT'

try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand

    class PyTest(TestCommand):
        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            # import here, cause outside the eggs aren't loaded
            import pytest
            errno = pytest.main(self.test_args)
            sys.exit(errno)
except ImportError:
    from distutils.core import setup

    def PyTest(x):
        x

setup(
    name='hoi4tools',
    zip_safe=False,
    version=version,
    author='Pierre-Francois Carpentier',
    author_email='carpentier.pf@gmail.com',
    packages=[
        'hoi4tools',
        'hoi4tools.cli',
        ],
    entry_points = {
        'console_scripts': [
            'hoi4-extract-raw = hoi4tools.cli.raw:main',
            'hoi4-extract-prod = hoi4tools.cli.prod_stats:main',
        ]
    },
    url='https://github.com/kakwa/python-hoi4tools',
    license=license,
    description=small_description,
    long_description=description,
    install_requires=install_requires,
    tests_require=['pytest', 'pep8', 'pytidylib'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        "Topic :: System :: Systems Administration"
        ],
)
