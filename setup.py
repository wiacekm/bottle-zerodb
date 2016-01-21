#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='bottle-zerodb',
    version='0.0.1',
    url='https://github.com/michalwiacek/bottle-zerodb',
    description='ZeroDB integration for Bottle',
    author='Michal Wiacek',
    author_email='michal.wiacek@gmail.com',
    license='MIT',
    platforms='any',
    py_modules=[
        'bottle_zerodb',
    ],
    install_requires=REQUIREMENTS,
    classifiers=[
        'Environment :: Web Environment',
        'Environment :: Plugins',
        'Framework :: Bottle',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
