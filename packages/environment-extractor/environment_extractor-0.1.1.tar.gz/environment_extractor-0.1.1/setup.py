#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Setuptools script for PEF library."""

import setuptools

with open("README.md", "r", encoding="iso-8859-1") as fh:
    long_description = fh.read()

setuptools.setup(
    name="environment_extractor",
    version="0.1.1",
    author="Joshua Brooke",
    author_email="joshua.brooke@outlook.com",
    description="Utility to create an environment.yml file from imports.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'stdlib_list',
    ],
    scripts=['environment_extractor/environment_extractor.py'],
    entry_points={
        'console_scripts': [
            'environment_extractor=environment_extractor.environment_extractor:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
