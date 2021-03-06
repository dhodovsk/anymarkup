#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='anymarkup',
    version='0.8.1',
    description='Parse/serialize any markup format',
    long_description=''.join(open('README.rst').readlines()),
    keywords='xml, yaml, toml, json, json5, ini',
    author='Slavek Kabrda',
    author_email='slavek.kabrda@gmail.com',
    url='https://github.com/bkabrda/anymarkup',
    license='BSD',
    packages=['anymarkup'],
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'anymarkup = anymarkup.cli:cli'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ]
)
