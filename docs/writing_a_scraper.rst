.. _writing a scraper:

Writing a scraper
=================

Overview
--------

*court-scraper*'s main goal is to serve as a framework for acquiring basic
court case metadata and raw file artifacts (e.g. HTML, JSON, PDFs, etc.) for county-level
courts.

These files can then be further processed in separate scripts that perform data extraction and standardization to
support the needs of a given project.

We're especially focused on platforms used by a large number of county court sites,
although we expect to create "one-off" scrapers for bespoke sites when necessary.

We also anticipate situations where county-level data simply isn't available online.
Such cases will require requesting data on a regular basis (and possibly paying for it).

If you're thinking of scraping a court site, it's important to conduct some research to determine what
data a court site provides. Some jurisdictions provide a simple search with case details readily accessible
online (and easily scrapable). Others provide multiple ways of accessing case data, such as a free and open
site that allows searching for case metadata, while hiding more detailed case information behind logins, CAPTCHAs,
paywalls, or some combination of these barriers.

Additionally, sites typically include legal restrictions on access and use of data.

When embarking on scraping a court site, it's important to understand their offerings and
the legal restrictions surrounding use of the site and its data. Please perform your due diligence
and reach out to discuss a particular site if you have questions about strategy!

Devise a scraping strategy
---------------------------

Before coding a new scraper, take some time to determine the best scraping strategy by interacting
with and `dissecting the site <https://github.com/stanfordjournalism/stanford-progj-2021/blob/main/docs/web_scraping/101.md>`_.

Whenever possible, we favor scrapers that gather data using basic HTTP GET or POST calls using
the Python requests_ library. Sites that are heavy on dynamically generated content and pose other
challenges may require browser automation via Selenium_. Such cases are unavoidable, although
often you may find it's possible to use a combination of both scraping strategies to optimize
the speed of the scraper. For example, the :py:class:`Wisconsin scraper <court_scraper.platforms.wicourts.site.Site>`
uses both libraries to achieve faster scrapes while handling (and minimizing the cost) of CAPTCHAs.

.. _requests: https://docs.python-requests.org/en/master/index.html
.. _Selenium: https://selenium-python.readthedocs.io/

Code a scraper
---------------

Add a Site class
~~~~~~~~~~~~~~~~

.. note:: Check out the docs for :ref:`getting started on code contributions <code contribution bootstrap>`
  for details on setting up a fork for local development.

The main task involved in contributing a scraper is creating a :code:`Site` class that
provides a :code:`search` method capable of scraping one or more case numbers.

For courts that offer date-based search, :code:`Site` should also have a :code:`search_by_date` method.
If the date search can be filtered by one or more case types, the method should include support for this
filter as well.

Lastly, sites that require login should have a :code:`login` method.

These methods should have `standard signatures <https://en.wikipedia.org/wiki/Type_signature#Method_signature>`_
in order to support automated scraping and for integration with *court-scraper*'s :ref:`commnand-line tool <cli>`.

Below is a simplified example of a scraper for an imaginary platform called *Court Whiz*. Each
method notes its expectations, and we use type annotations to signal expected return values::

    # court_scraper/platforms/court_whiz/site.py

    from typing import List
    from court_scraper.case_info import CaseInfo

    class Site:

        def __init__(self, place_id):
            self.place_id = place_id
            self.url = "https://court-whiz.com"

        def search(self, case_numbers=[]) -> List[CaseInfo]:
            # Perform a place-specific search (using self.place_id)
            # for one or more case numbers.
            # Return a list of CaseInfo instances containing case metadata and,
            # if available, HTML for case detail page
            pass

        def search_by_date(self, start_date=None, end_date=None, case_details=False, case_types=[]) -> List[CaseInfo]:
            # Perform a place-specific, date-based search.
            # Defaut to current day if start_date and end_date not supplied.
            # Only scrape case metadata from search results pages by default.
            # If case_details set to True, scrape detailed case info
            # Apply case type filter if supported by site.
            # Return a list of CaseInfo instances
            pass

        def login(self, username, password):
            # Perform login with username and password
            pass


Site classes for scrapers specific to a single county should live in
the :code:`court_scraper.scrapers` namespace under a package based on the jurisdiction's
:ref:`Place ID <place id>`.

For example, the Site class for Westchester County would live in :code:`court_scraper.scrapers.ny_westchester.site.py`.

Many counties use common software platforms, such as Odyssey by Tyler Technologies, to provide case information.

To add a platform-based scraper for use in more than one jurisdiction, add a site class to the :code:`court_scraper.platforms` namespace.
For example, :py:class:`court_scraper.platforms.odyssey.site.Site`.

.. note:: We've provided some base classes and helper functions to help with common
   scenarios (e.g. see :py:class:`SeleniumHelpers <court_scraper.base.selenium_helpers.SeleniumHelpers>` and functions
   in :py:mod:`court_scraper.utils`).

Add tests
~~~~~~~~~

New site classes should include test coverage for the :code:`search` and :code:`search_by_date` methods.

Check out our :ref:`Testing docs <testing>` and review test modules for the Odyssey, Oklahoma (oscn) or Wisconsin (wicourts)
site classes for examples that can help you get started.

Update *court_scraper.site.Site*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :py:class:`court_scraper.site.Site` class provides a simpler interface for looking up and working
with a jurisdiction's Site class.

If your new Site class has some initialization needs beyond simply providing a :ref:`Place ID <place id>`,
you may need to update :py:class:`court_scraper.site.Site` with special handling for your new Site class.

Even if you don't update :py:class:`court_scraper.site.Site`, it's a good idea to add at least one
high-level integration test in :code:`tests/test_site.py` for your new Site class to ensure it's
handled correctly.

CLI Integration
---------------

Integration with *court-scraper*'s :ref:`command-line tool <cli>` requires several steps, as detailed
below.

Create a Runner
~~~~~~~~~~~~~~~~

First, you must create a :code:`Runner` class capable of driving the newly implemented :code:`Site`
class. Runners generally perform the following taks:

- Instantiate the :code:`Site` class
- Call :code:`Site.search` with values passed in by :py:mod:`court_scraper.cli`
- Set sensible defaults, as needed
- Perform caching of scraped file artifacts
- Log information to the command-line, as needed

See the runners for :py:class:`Oklahoma <court_scraper.platforms.oscn.runner.Runner>`
or :py:class:`Odyssey <court_scraper.platforms.odyssey.runner.Runner>` for reference implementations.


Sites Meta CSV
~~~~~~~~~~~~~~~

In order for our CLI tool to execute scrapes for a given jurisdiction, the jurisdiction
must be added to `sites_meta.csv`_. This file contains the following fields:

- :code:`state` - 2-letter state abbreviation, lower cased
- :code:`county` - lower-case name of county (without the word "County")
- :code:`site_type` - Base name of the Python package where the Site class lives (e.g. `odyssey` or `wicourts`)
- :code:`site_version` - Platform based sites may have multiple versions. Use this field to denote a new version of a platform-based site.
- :code:`captcha_service_required` - Mark as True if a site presents CAPTCHAs
- :code:`home_url` - Starting page for a platform used by many jurisdictions at separate domains (e.g. `odyssey`)


It's important to note that *every jurisdiction covered* by a scraper
must be entered in `sites_meta.csv`_, even if the sites share a common
platform.

For example, there are separate entries in `sites_meta.csv`_ for most counties in Washington State. These
jurisdictions use the Odyssey platform, but they live at different domains. `sites_meta.csv`_ provides a single
place to store the home URL and other metadata for each of these counties.


.. _sites_meta.csv: https://github.com/biglocalnews/court-scraper/blob/master/court_scraper/data/sites_meta.csv
