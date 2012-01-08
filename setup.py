#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

import api2ch

setup(name="api2ch",
      description="Object oriented wrapper for 2ch.so json-api",
      long_description=open("README.rst").read(),
      author=api2ch.__author__,
      version=api2ch.__version__,
      author_email="d1fffuz0r@gmail.com",
      py_modules=["api2ch"],
      url="https://github.com/d1ffuz0r/2ch-API",
      classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: API",
        "Topic :: Software Development :: Libraries :: Python Modules"
      ])
