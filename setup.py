from os import path

from setuptools import setup

from api2ch import __author__, __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

requires = ['requests', 'addict', 'simplejson']

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
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet'
    ],
    zip_safe=False
)
