#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages

import api2ch

setup(name=api2ch.__doc__,
      description="Object oriented wrapper for 2ch.so json-api",
      long_description=open("README").read(),
      author=api2ch.__author__,
      version=api2ch.__version__,
      author_email="d1fffuz0r@gmail.com",
      py_modules=["api2ch"],
      url="http://github.com/d1ffuz0r/api2ch",
      license="GNU/GPL v3",
      platforms="Linux, Windows, Max OS X",
      classifiers=[
        "License :: GNU/GPL v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: API",
        "Topic :: Software Development :: Libraries :: Python Modules"
      ])
