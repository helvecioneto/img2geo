#!/usr/bin/env python3
# -*- Coding: UTF-8 -*-
import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="img2geo",
    license="Apache License 2.0",
    version='1.0',
    author='Helvecio B L Neto',
    author_email='helvecio.neto@inpe.br',
    packages=find_packages("src"),
    package_dir={"":"src"},
    description="Convert PNG Files to GeoTiff",
    lond_description=read("README.md"),
    install_requires=["numpy",
                      "pyproj",
                      "geopy",
                      "gdal",
                      "osr",
		      ]
)