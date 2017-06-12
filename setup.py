#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


requirements = [
    "requests"
]

setup(
    name='fin360',
    version='0.1.0',
    description="",
    long_description='',
    author="Kshitij Mittal",
    author_email='kshitij@loanzen.in',
    url='https://github.com/loanzen/fin360-py',
    packages=[
        'fin360',
    ],
    package_dir={'fin360':
                 'fin360'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)
