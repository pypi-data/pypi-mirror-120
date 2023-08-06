#!/usr/bin/env python3

import minorimpact
from setuptools import find_packages, setup

setup(
    name='minorimpact',
    packages=find_packages(include=['minorimpact']),
    version=minorimpact.__version__,
    description='Personal utility library',
    author='Patrick Gillan',
    author_email = 'pgillan@minorimpact.com',
    license='GPLv3',
    install_requires=[],
    setup_requires=[],
    tests_require=[],
)
