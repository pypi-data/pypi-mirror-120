#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='mumuzi',
    version='0.0.1',
    author='mumuzi_fans',
    author_email='mumuzi@mumuzi.mumuzi',
    url='https://blog.csdn.net/qq_42880719/',
    description=u'CTF全栈全自动解题姬mumuzi',
    packages=['mumuzi'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'hello=mumuzi:hello'
        ]
    }
)