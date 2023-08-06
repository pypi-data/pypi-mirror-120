#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author jsbxyyx
import os

import setuptools

VERSION = "0.1.1"

base_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base_dir, "README.md"), "r") as f:
    long_description = f.read()

with open(os.path.join(base_dir, "requirements.txt"), "r") as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="antlr4-mysql",
    version=VERSION,
    author="jsbxyyx",
    author_email="jsbxyyx@163.com",
    license="Apache License 2.0",
    description="antlr4-mysql",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    url="https://github.com/jsbxyyx/antlr4-mysql",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
