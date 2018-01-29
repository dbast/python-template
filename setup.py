# -*- coding: utf-8 -*-

"""setup.py is Python's answer to a multi-platform make file and installer"""

# prefer setuptools over distutils
from setuptools import setup
import versioneer

setup(
    name='python-template',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Starting point for Python projects',
    url='https://github.com/dbast/python-template',
    author='Daniel Bast',
    author_email='2790401+dbast@users.noreply.github.com',
    license='MIT',
    packages=['examples'],
    install_requires=['boto3'],

    setup_requires=[
        'pytest-runner',
        'pytest-pylint'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'mock'
    ],
    entry_points={
        'console_scripts': [
            'clusters=examples.clusters:cli'
        ],
    },
)
