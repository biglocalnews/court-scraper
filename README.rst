
.. image:: https://img.shields.io/pypi/v/court-scraper.svg
        :target: https://pypi.python.org/pypi/court-scraper

.. image:: https://img.shields.io/pypi/pyversions/court-scraper.svg
        :target: https://pypi.python.org/pypi/court-scraper

.. image:: https://img.shields.io/travis/biglocalnews/court-scraper.svg
        :target: https://travis-ci.com/biglocalnews/court-scraper

.. image:: https://readthedocs.org/projects/court-scraper/badge/?version=latest
        :target: https://court-scraper.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://badges.gitter.im/court-scraper/general.svg
        :target: https://gitter.im/court-scraper/general?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
        :alt: Gitter

=============
Court Scraper
=============

Overview
========

The `court-scraper` package provides a Python library and command-line
tool that help search for and download case information from local court system
websites in the United States. This library primarily focuses on supporting the ability
to scrape county-level court data by case number and date range.

* Documentation: http://court-scraper.readthedocs.io/en/latest/
* GitHub: https://github.com/biglocalnews/court-scraper
* PyPI: https://pypi.python.org/pypi/court-scraper
* Free and open source software: `Apache license`_

.. _Apache license: https://github.com/biglocalnews/court-scraper/blob/master/LICENSE

Pre-reqs
========

* Python >= 3.6
* Scrapers that rely on Selenium require:

  * `Google Chrome <https://www.google.com/chrome/>`_ web browser
  * `Chromedriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`_

.. _Pipenv: https://pipenv.pypa.io/en/latest/

Quickstart
==========

Install court-scraper_::

   pip install court-scraper

Scrape using the command line tool::

   # Scrape data for a case in Tulsak, Oklahoma
   $ court-scraper search -p ok_tulsa -s CJ-2021-2045

Or in a script::

  # awesome-scraper-script.py

  # Scrape case details from Oklahoma State Courts Network (OSCN) platform

  from court_scraper import Site

  site = Site('ok_tulsa')

  # Scrape details for one or more case numbers
  results = site.search(case_numbers=['CJ-2021-2045'])

  # Scrape details for cases in January 2021
  results = site.search_by_date(
    start_date='2021-01-01,
    end_date='2021-01-31',
    case_details=True
  )

.. note:: Check out the :ref:`usage` docs for more detailed information on scraping.


.. _court-scraper: https://github.com/biglocalnews/court-scraper
.. _court-scraper docs: https://court-scraper.readthedocs.io/en/latest/
