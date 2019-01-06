from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

__author__ = 'anonim-legivon'

__version__ = '1.0.0'

requires = [
    'requests==2.21.0',
    'addict==2.2.0',
    'simplejson==3.16.0'
]

setup(
    name='dvach.api',
    version=__version__,
    python_requires='>=3.6',
    packages=['api2ch'],
    package_data={'': ['LICENSE']},
    package_dir={'dvach.api': 'api2ch'},
    url='https://github.com/anonim-legivon/dvach.api',
    license='Apache License 2.0',
    author=__author__,
    author_email='fadedDexofan@protonmail.com',
    include_package_data=True,
    install_requires=requires,
    description='Python 2ch.hk API wrapper',
    long_description=long_description,
    keywords='dvach 2ch 2ch.hk api wrapper',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet'
    ],
    zip_safe=False
)
