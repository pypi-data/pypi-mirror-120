#!/usr/bin/env python
import numpy
import sys
from setuptools import setup, find_packages, Extension


# Setup C module include directories
include_dirs = [numpy.get_include()]

# Setup C module macros
define_macros = [('NUMPY', '1')]

# Handle MSVC `wcsset` redefinition
if sys.platform == 'win32':
    define_macros += [
        ('_CRT_SECURE_NO_WARNING', None),
        ('__STDC__', 1)
    ]

PACKAGE_DATA = {'': ['README.md', 'LICENSE.txt']}

setup(
    use_scm_version={"write_to": "stsci/imagestats/_version.py"},
    setup_requires=['setuptools_scm'],
    package_data=PACKAGE_DATA,
    ext_modules=[
        Extension('stsci.imagestats.buildHistogram',
                  ['src/buildHistogram.c'],
                  include_dirs=include_dirs,
                  define_macros=define_macros),
        Extension('stsci.imagestats.computeMean',
                  ['src/computeMean.c'],
                  include_dirs=include_dirs,
                  define_macros=define_macros),
    ],
)
