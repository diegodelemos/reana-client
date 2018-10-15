# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017, 2018 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REANA client"""

from __future__ import absolute_import, print_function

import os
import re

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'docutils>=0.14',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0,<3.0.0'
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
        'sphinx-rtd-theme>=0.1.9',
        'sphinx-click>=1.0.4',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for key, reqs in extras_require.items():
    if ':' == key[0]:
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.7',
]

install_requires = [
    'click>=6.7,<6.8',
    'cwltool==1.0.20180912090223',
    'pyOpenSSL==17.3.0',  # FIXME remove once yadage-schemas solves deps.
    'reana-commons>=0.4.0.dev20181011,<0.5.0',
    'rfc3987==1.3.7',  # FIXME remove once yadage-schemas solves deps.
    'strict-rfc3339==0.7',  # FIXME remove once yadage-schemas solves deps.
    'tablib>=0.12.1,<0.13',
    'webcolors==1.7',  # FIXME remove once yadage-schemas solves deps.
    'yadage-schemas==0.7.16',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
with open(os.path.join('reana_client', 'version.py'), 'rt') as f:
    version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        f.read()
    ).group('version')

setup(
    name='reana-client',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    author='REANA',
    author_email='info@reana.io',
    url='https://github.com/reanahub/reana-client',
    packages=['reana_client', ],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'reana-client = reana_client.cli:cli',
            'reana-cwl-runner = reana_client.cli.cwl_runner:cwl_runner'
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
