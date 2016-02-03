#!/usr/bin/env python
from setuptools import setup

VERSION = '0.0.1'


tests_requires = [
    'nose>=1.3.4',
    'responses>=0.5.1'
]

install_requires = [
    'requests>=2.4.3',
]

setup(
    name="mondo",
    version=VERSION,
    description="Mondo Banking API Client",
    author=', '.join((
        'Tito Miguel Costa',
        'Simon Vans-Colina <simon@simon.vc>',
    )),
    url="https://github.com/simonvc/mondo-python",
    packages=["mondo"],
    tests_require=tests_requires,
    install_requires=install_requires,
    license="MIT",
)
