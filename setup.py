#!/usr/bin/env python
from setuptools import setup

VERSION = '0.0.1'

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
    install_requires=['requests>=2.4.3'],
    license="MIT",
)
