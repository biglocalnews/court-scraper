.. _usage:

Usage
=====

Overview
--------

*court-scraper* provides a command-line tool and underlying Python library
that can be used to scrape data about court cases.  The command-line tool makes it easy
to get started scraping for basic use cases, while the Python library offers a wider range of options
for use in custom scripts.

Our project focuses mainly on scraping software platforms used by multiple jurisdictions
or statewide systems that cover all counties.

These platforms vary in terms of supported features. Some provide only basic search by party or case number,
whereas others support numerous search parameters, including date-based searches.

Wherever possible, `court-scraper` attempts to provide support for search by:

- **date range** - to enable automated discovery of new cases and backfilling of previous cases.
- **case type** - to enable more targeted scrapes in combination with date range
- **case number** - to enable ongoing updates of open cases

The library is currently focused on acquring raw file artifacts (e.g. HTML or JSON files containing case data).
Extracting and standardizing particular data points from these raw files is currently not handled by the
`court-scraper` framework, and must be handled by the end user.

.. note:: We hope to eventually provide tools to help with data extraction and standardization. However,
          due to the wide variability of case types even within a single platform, this effort remains
          on our long-term roadmap. We welcome :ref:`contributions <contributing>` on this front!


.. _find a site:

Find a court to scrape
-----------------------

Before you can start scraping court records, you must first pinpoint
a county of interest and check whether we currently support it.

Use the command-line tool's :ref:`info sub-command <cli info>` to list currently supported counties.

If you don't see the state or county you're targeting, it's worth checking out our `Issue tracker`_ to
see if it's on the roadmap. In some cases, we may be actively working on adding support for your jurisdiction. We also
have a stable of scrapers that were written by others for project-specific purposes and contributed
to our project for integration into our more general framework. We can provide access to these
"one-off" scrapers for your customization, even if we have not yet integrated them into `court-scraper`.

.. _Issue tracker: https://github.com/biglocalnews/court-scraper/issues


.. _place id:

Place IDs
---------

*court-scraper* requires searches to target courts/jurisdictions in specific counties. Every jurisdiction supported
by the framework has a so-called `Place ID`. These unique identifiers are in "snake case" format
(i.e. lower case with underscores): :code:`<state_postal>_<county_name`.

For example, the `Place ID` for Tulsa, Oklahoma is :code:`ok_tulsa`.

Whether working with the :ref:`CLI` or :ref:`Custom scripts`, you'll need to identify the `Place ID` for the
target jurisdiction. You can use the command-line tool's :ref:`info sub-command <cli info>` to
find the `Place ID` for your jurisdiction.


.. _cli:

Command line
------------

The command-line tool makes it easy to get started scraping for basic use cases.

Once you :ref:`install <install>` *court-scraper* and
:ref:`find a court site to scrape <find a site>`, you're ready to begin
using the command-line tool.

.. _cli info:

Info command
~~~~~~~~~~~~

The command-line tool includes an :code:`info` sub-command that lists the currently supported counties::

  # List all supported counties
  court-scraper info

.. note:: See :ref:`find a site` for advice if your jurisdiction is not among those listed.


Case number search
~~~~~~~~~~~~~~~~~~

The *court-scraper* CLI's :code:`search` sub-command is the primary way to gather
case details from a county court site. You can use the tool's :code:`--help`
flag to get details on the available options::

  court-scraper search --help

The :code:`search` sub-command supports scraping case details by case number. It requires two parameters:

- :code:`--place-id` or :code:`-p` - A combination of state postal and county name in "snake case" (e.g. `ok_tulsa`). The :code:`place-id` can be obtained by using the :ref:`info sub-command <cli info>`.

- :code:`--case-number` or :code:`-c` - A single case number to scrape.

Here's an example search for Tulsa, Oklahoma::

  # Scrape case details by place ID and case number
  court-scraper search --place-id ok_tulsa --case-number CJ-2021-2045

To search for more than one case at a time, use the :code:`--case-numbers-file` (or :code:`-f`) flag
with a text file containing case numbers on separate lines.

For example, if you have a text file with these case numbers::

  # case_numbers.txt
  CJ-2021-2045
  CJ-2021-2046

Search using the `case_numbers.txt` file::

  court-scraper search --place-id ok_tulsa --case-numbers-file case_numbers.txt


Browser mode
~~~~~~~~~~~~

Scrapers that use `Selenium <https://selenium-python.readthedocs.io/>`_ to drive a web browser
by default run in "headless" mode (i.e. the browser will not run visibly). In order
to run a Selenium-based scraper with the browser, which can be helpful for debugging, use
the :code:`--with-browser` flag::

  court-scraper search --with-browser --place-id ok_tulsa --case-number CJ-2021-2045


File storage
~~~~~~~~~~~~~

Files scraped by the :code:`search` sub-command are saved to a :ref:`standard <default cache dir>`  -- but :ref:`configurable <customize cache dir>` -- location 
in the user's home directory (:code:`~/.court-scraper` on Linux/Mac).

Metadata db
~~~~~~~~~~~~

The :code:`search` sub-command stores basic metadata about scraped cases in a SQLite database
located in the :ref:`standard cache directory <default cache dir>`: :code:`~/.court-scraper/cases.db`.

The database can be helpful for quickly checking which cases have been scraped.

It stores the following fields:

* ``created`` (*datetime*) - The date and time of the case was initially scraped.
* ``udpated`` (*datetime*) - The date and time of last scrape for the case.
* ``place_id`` (*str*) - The state postal and county name in "snake case" (e.g. `ok_tulsa`).
* ``number`` (*str*) - The case number.
* ``filing_date`` (*date*) - The filing date of the case (if available).
* ``status`` (*str*) - Case status (if available).

.. _custom scripts:

Custom scripts
--------------

*court-scraper* provides an importable Python package for users who are comfortable creating their 
own scripts. The Python package provides access to a wider variety of features for
added flexibility and more advanced scenarios:

- Searching by date
- Filtering by case type
- Scraping only case metadata (i.e. not gathering case details, which generally takes longer)

.. note:: The above features are not supported by all sites, so it's important to familiarize
   yourself with the site and our Pythonic wrappers to get a sense of available features for
   a given jurisdiction.


Scrape cases
~~~~~~~~~~~~

Once you :ref:`install <install>` *court-scraper* and
:ref:`find a site to scrape <find a site>`, you're ready to begin
using the ``court_scraper`` Python package.

Create an instance of :code:`Site` by passing it the :ref:`Place ID <place id>` for
the jurisdiction. Then call the :code:`search` method with one or more case numbers::

  from court_scraper import Site
  site = Site('ok_tulsa')
  case_numbers=['CJ-2021-1904', 'CJ-2021-1905']
  results = site.search(case_numbers=case_numbers)

.. note:: :code:`Site` provides a generic interface to simplify import and configuration
   of platform-specific Site classes, such as :py:class:`court_scraper.platforms.oscn.site.Site`.
   Platform Site classes typically have varying options for initialization and search, so it's a good
   idea to review their options when using this generic Site interface.
   :py:meth:`oscn.Site.search <court_scraper.platforms.oscn.site.Site.search>`, for example, 
   does FOO TK.


Scrape by date
~~~~~~~~~~~~~~

Some sites support date-based search. In such cases,
you can use the platform's :code:`Site.search_by_date` method
to scrape data for one or more days.

The default is to search for cases on the current day::

  from court_scraper import Site
  site = Site('ok_tulsa')
  results = site.search_by_date()


Supplying the optional :code:`start_date` and/or :code:`end_date` arguments
to :py:meth:`oscn.Site.search <court_scraper.platforms.oscn.site.Site.search>`.

Their values must be strings of the form :code:`YYYY-MM-DD`::

  from court_scraper import Site
  site = Site('ok_tulsa')
  results = site.scrape(start_date='2020-01-01', end_date='2020-01-30')


TODO:

- scrape metadata only (i.e. case_details flag)
- RTD on site classes to customize init, search and search_by_date kwargs
