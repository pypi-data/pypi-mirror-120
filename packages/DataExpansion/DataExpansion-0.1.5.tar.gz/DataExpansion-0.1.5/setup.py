#!/usr/bin/env python
# -*- coding:utf-8 -*-
from glob import glob
from os import name
from os.path import basename
from os.path import splitext
from sys import version

from setuptools import setup
from setuptools import find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name="DataExpansion",
    version="0.1.5",
    license="Apache License",
    description="SQLを利用してクラスを保存します",
    long_description=readme,
    author="TangentMochi",
    author_email="yu180609@gmail.com",
    url="https://github.com/TangentMochi/DataExpansion",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Database",
        "Natural Language :: Japanese",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 1 - Planning",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"]
)