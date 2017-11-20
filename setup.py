from setuptools import setup

from api2ch import api2ch

install_requires = [
    'requests>=2.8.1'
]

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
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: API',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
