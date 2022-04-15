#!/usr/bin/env python
"""
.. image:: https://img.shields.io/pypi/v/court-scraper.svg
        :target: https://pypi.python.org/pypi/court-scraper
        :alt: PyPI version badge

.. image:: https://img.shields.io/pypi/pyversions/court-scraper.svg
        :target: https://pypi.python.org/pypi/court-scraper
        :alt: Python versions badge

.. image:: https://github.com/biglocalnews/court-scraper/actions/workflows/tests.yaml/badge.svg?branch=master
        :target: https://github.com/biglocalnews/court-scraper/actions/workflows/tests.yaml
        :alt: GitHub Actions build status badge

.. image:: https://readthedocs.org/projects/court-scraper/badge/?version=latest
        :target: https://court-scraper.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://badges.gitter.im/court-scraper/general.svg
        :target: https://gitter.im/court-scraper/general?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
        :alt: Gitter badge


Court Scraper
-------------

The `court-scraper` package provides a Python library and command-line
tool that help search for and download case information from local court system
websites in the United States. This library primarily focuses on supporting the ability
to scrape county-level court data by case number and date range.

* Documentation: http://court-scraper.readthedocs.io/en/latest/
* GitHub: https://github.com/biglocalnews/court-scraper
* PyPI: https://pypi.python.org/pypi/court-scraper
* Gitter: https://gitter.im/court-scraper/general
* Free and open source software: `Apache license`_

.. _Apache license: https://github.com/biglocalnews/court-scraper/blob/master/LICENSE

"""
from setuptools import find_packages, setup

requirements = [
    "anticaptchaofficial",
    "bs4",
    "click",
    "click-option-group",
    "cssselect",
    "lxml",
    "my-fake-useragent",
    "pyyaml",
    "retrying",
    "selenium",
    "sqlalchemy",
    "typing-extensions",
]


test_requirements = ["flake8", "pytest", "pytest-vcr"]


setup(
    name="court-scraper",
    version="0.1.1",
    description="Command-line tool for scraping data from U.S. county courts",
    long_description=__doc__,
    long_description_content_type="text/x-rst",
    author="Serdar Tumgoren",
    author_email="zstumgoren@gmail.com",
    url="https://github.com/biglocalnews/court-scraper",
    packages=find_packages(),
    package_data={"court_scraper": ["data/*.csv"]},
    entry_points="""
        [console_scripts]
        court-scraper=court_scraper.cli:cli
    """,
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    project_urls={
        "Maintainer": "https://github.com/biglocalnews",
        "Source": "https://github.com/biglocalnews/court-scraper",
        "Tracker": "https://github.com/biglocalnews/court-scraper/issues",
    },
)
