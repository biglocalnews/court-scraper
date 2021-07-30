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

- :code:`--search-term` or :code:`-s` - A search term (i.e. a single case number).

Here's an example search for Tulsa, Oklahoma::

  # Scrape case details by place ID and case number
  court-scraper search --place-id ok_tulsa --search-term CJ-2021-2045

To search for more than one case at a time, use the :code:`--search-terms-file` (or :code:`-f`) flag
with a text file containing case numbers on separate lines.

For example, if you have a text file with these case numbers::

  # case_numbers.txt
  CJ-2021-2045
  CJ-2021-2046

Search using the `case_numbers.txt` file::

  court-scraper search --place-id ok_tulsa --search-terms-file case_numbers.txt


Browser mode
~~~~~~~~~~~~

Scrapers that use `Selenium <https://selenium-python.readthedocs.io/>`_ to drive a web browser
by default run in "headless" mode (i.e. the browser will not run visibly). In order
to run a Selenium-based scraper with the browser, which can be helpful for debugging, use
the :code:`--with-browser` flag::

  court-scraper search --with-browser --place-id ok_tulsa --search-term CJ-2021-2045


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


Identify the site class
~~~~~~~~~~~~~~~~~~~~~~~

Each court jurisdiction has a site class that serves as the main entry point for scraping.
To determine which class.

Scrape metadata
~~~~~~~~~~~~~~~

Once you :ref:`install <install>` *court-scraper* and
:ref:`find a site to scrape <find a site>`, you're ready to begin
using the ``court_scraper`` Python package.

Create an instance of :code:`OdysseySite` by passing it the URL for an
court's home page.  Then call the :code:`scrape` method::

  from court_scraper.platforms import CivicPlusSite
  url = 'https://ca-eastpaloalto.civicplus.com/AgendaCenter'
  site = CivicPlusSite(url)
  assets_metadata = site.scrape()

.. note:: :code:`CivicPlusSite` is an alias for more convenient import of the actual Civic Plus class
   located at :py:class:`court_scraper.platforms.court_plus.site.Site`.

:py:meth:`CivicPlusSite.scrape <court_scraper.platforms.court_plus.site.Site.scrape>` will automatically store 
downloaded assets in the :ref:`default cache directory <default cache dir>`. 

This location can be customized by :ref:`setting an environment variable <customize cache dir>` or by passing an
instance of :py:class:`court_scraper.base.cache.Cache` to :py:class:`CivicPlusSite <court_scraper.platforms.court_plus.site.Site>`::
  
  from court_scraper.base.cache import Cache
  from court_scraper.platforms import CivicPlusSite

  url = 'https://ca-eastpaloalto.civicplus.com/AgendaCenter'

  # Change output dir to /tmp
  site = CivicPlusSite(url, cache=Cache('/tmp'))
  assets_metadata = site.scrape()


.. _export metadata script:

Export metadata to CSV
~~~~~~~~~~~~~~~~~~~~~~

By default, :py:meth:`CivicPlusSite.scrape <court_scraper.platforms.court_plus.site.Site.scrape>` returns an :py:class:`~court_scraper.base.asset.AssetCollection` 
containing :py:class:`~court_scraper.base.asset.Asset` instances. 

The asset instances store metadata about specific meeting agendas and 
minutes discovered on the site.

To save a timestamped CSV containing metadata for available assets, 
call :py:meth:`AssetCollection.to_csv() <court_scraper.base.asset.AssetCollection.to_csv>` with a target output directory::

  # Save metadata CSV
  assets_metadata.to_csv('/tmp/civic-scraper/metadata')

.. _download assets script:

Download assets
~~~~~~~~~~~~~~~

There are two primary ways to download file assets discovered by a scrape. 

You can trigger downloads by passing :code:`download=True` to
:py:meth:`CivicPlusSite.scrape <court_scraper.platforms.court_plus.site.Site.scrape>`::

  site.scrape(download=True)

Or you can loop over the :py:class:`Asset instances <court_scraper.base.asset.Asset>`
in an :py:class:`~court_scraper.base.asset.AssetCollection` and 
call :py:meth:`~court_scraper.base.asset.Asset.download` on each with a target output directory::

  assets_metadata = site.scrape()
  for asset in assets_metadata:
      asset.download('/tmp/civic-scraper/assets')

Scrape by date
~~~~~~~~~~~~~~

By default, scraping checks the site for meetings on the current day (based on a
user's local time).

Scraping can be modified to capture assets from different date ranges by
supplying the optional :code:`start_date` and/or :code:`end_date` arguments
to :py:meth:`CivicPlusSite.scrape <court_scraper.platforms.court_plus.site.Site.scrape>`. 

Their values must be strings of the form :code:`YYYY-MM-DD`::

  # Scrape info from January 1-30, 2020
  assets_metadata = site.scrape(start_date='2020-01-01', end_date='2020-01-30')

.. note:: The above will *not* download the assets by default. See :ref:`download assets script` for details
   on saving the discovered files locally.

Advanced configuration
~~~~~~~~~~~~~~~~~~~~~~

You can exercise more fine-grained control over the size and type of files to download
using the :code:`file_size` and :code:`asset_list` arguments to
:py:meth:`CivicPlusSite.scrape <court_scraper.platforms.court_plus.site.Site.scrape>`::


  # Download only minutes that are 20MB or smaller
  site.scrape(
    download=True,
    file_size=20,
    asset_list=['minutes']
  )

Here are more details on the parameters mentioned above:

* :code:`file_size` - Limit downloads to files with max file size in megabytes.
* :code:`asset_list` -  Limit downloads to one or more `asset types`_ 
  (described below in `Metadata CSV`_). The default is to download all document types.

.. _metadata csv:


.. _change download dir:

Changing the download location
-------------------------------

By default, *civic-scraper* will store downloaded agendas, minutes and 
other files in a :ref:`default directory <default cache dir>`.

You can :ref:`customize this location <customize cache dir>` by setting 
the :code:`court_SCRAPER_DIR` environment variable.
