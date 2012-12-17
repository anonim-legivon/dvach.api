#!/usr/bin/env python

from setuptools import setup

import api2ch
import sys

test_require = ['mock'] if sys.version_info.major == 2 else []

setup(name='api2ch',
      description='Object oriented wrapper for 2ch.so json-api',
      long_description=open('README.rst').read(),
      author=api2ch.__author__,
      version=api2ch.__version__,
      author_email='d1fffuz0r@gmail.com',
      py_modules=['api2ch'],
      url='https://github.com/d1ffuz0r/2ch-API',
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: API',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      zip_safe=False,
      tests_require=test_require,
      test_suite='tests')
