#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(file_name):
    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, file_name)
    with open(file_path) as f:
        return f.read()


requirements = [
    'anticaptchaofficial',
    'click',
    'click-option-group',
    'lxml',
    'my-fake-useragent',
    'pyyaml',
    'retrying',
    'selenium',
    'sqlalchemy'
]


test_requirements = [
    'flake8',
    'pytest',
    'pytest-vcr'
]


setup(
    name='court-scraper',
    version='0.1.0',
    description="Command-line tool for scraping data from U.S. county courts",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    project_urls={
        'Maintainer': 'https://github.com/biglocalnews',
        'Source': 'https://github.com/biglocalnews/court-scraper',
        'Tracker': 'https://github.com/biglocalnews/court-scraper/issues'
    },
)
