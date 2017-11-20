from os import path

from setuptools import setup

from api2ch import api2ch

here = path.abspath(path.dirname(__file__))

install_requires = [
    'requests>=2.8.1'
]
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dvach.api',
    version=api2ch.__version__,
    python_requires='>=3.5',
    packages=['api2ch'],
    url='https://github.com/anonim-legivon/dvach.api',
    license='Apache License 2.0',
    author=api2ch.__author__,
    author_email='fadedDexofan@protonmail.com',
    py_modules=['api2ch'],
    install_requires=install_requires,
    description='Python 2ch.hk API wrapper',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet'

    ]
)
