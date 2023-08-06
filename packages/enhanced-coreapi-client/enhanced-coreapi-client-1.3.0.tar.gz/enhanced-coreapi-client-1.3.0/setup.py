#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import os
from setuptools import setup, find_packages

__doc__ = 'Enhanced CoreAPI client'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


readme = read('README.rst')
changelog = read('CHANGELOG.rst')
version = read('VERSION').strip()

install_requires = [
    'coreapi>=2.3',
]

dev_require = [
    'ipython',
]

extras_require = {
    'dev': dev_require,
}


setup(
    name='enhanced-coreapi-client',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + changelog,
    author='murchik',
    author_email='murchik@protonmail.com',
    url='https://gitlab.com/murchik/enhanced-coreapi-client',
    packages=[package for package in find_packages()],
    install_requires=install_requires,
    extras_require=extras_require,
    license='GNU General Public License v3 (GPLv3)',
    zip_safe=True,
    keywords='enhanced-coreapi-client',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
