#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
    'anticaptchaofficial',
    'bs4',
    'click',
    'click-option-group',
    'lxml',
    'my-fake-useragent',
    'pyyaml',
    'retrying',
    'selenium',
    'sqlalchemy',
    'typing-extensions'
]

test_requirements = [
    'flake8',
    'pytest',
    'pytest-vcr'
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
    package_data={'court_scraper': ['data/*.csv']},
    entry_points='''
        [console_scripts]
        court-scraper=court_scraper.cli:cli
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
    ],
    test_suite='tests',
    tests_require=test_requirements
)
