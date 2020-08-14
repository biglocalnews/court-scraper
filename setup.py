#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
    'click',
    'lxml',
    'my-fake-useragent',
    'pyyaml',
    'retrying',
    'selenium',
]

test_requirements = [
    'flake8',
    'pytest',
#    'vcrpy',
#    'pytest-vcr'
]

setup(
    name='court-scraper',
    version='0.1.0',
    description="Command-line tool for scraping data from U.S. county courts.",
    long_description=__doc__,
    author="Serdar Tumgoren",
    author_email='zstumgoren@gmail.com',
    url='https://github.com/biglocalnews/court-scraper',
    packages=find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        court-scraper=court_scraper.cli:main
    ''',
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
