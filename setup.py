#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from distutils.core import setup
import glob
from setuptools import setup

readme = open('README.md').read()

setup(
    name='edamxpathvalidator',
    version='0.1',
    description='validation of EDAM internal consistency',
    long_description=readme,
    author='Hervé Ménager',
    author_email='hmenager@pasteur.fr',
    url='https://github.com/edamontology/ReMoTE.git',
    packages=['edamxpathvalidator'],
    install_requires=[
          'lxml'
    ],
    license="BSD",
    entry_points={
          'console_scripts': ['edamxpathvalidator=edamxpathvalidator:main'],
        },
    include_package_data=True,
    zip_safe=False 
)
