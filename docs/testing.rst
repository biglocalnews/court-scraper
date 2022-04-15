.. _testing:

Testing
=======

Overview
--------

*court-scraper* is developed primarily on Python 3.7 and uses the pytest_ library for unit testing.
We use pytest-vcr_ for scrapers that use the `requests` library
(e.g. :py:class:`oscn.Site <court_scraper.platforms.oscn.site.Site>`). Scrapers that
use Selenium should include a minimal set of :ref:`live webtests <live tests>` to ensure
correct functionality and guard against regressions.

.. note:: Selenium and other long-running tests should be marked as :ref:`slow <slow tests>`
    to enable optional running of these tests.

.. _pytest: https://docs.pytest.org/en/latest/contents.html
.. _pytest-vcr: https://github.com/ktosiek/pytest-vcr

Install and run tests
----------------------

Assuming you've cloned this repo locally and installed test and application dependencies,
you can run tests by executing pytest in an active virtual environment::

    cd court-scraper/
    pipenv install --dev

    # Execute tests
    pipenv run pytest

.. _slow tests:

Slow tests
----------

Slow-running tests should be marked_ as such::

    @pytest.mark.slow
    def test_something_slow():
        ...


Slow tests are skipped by default. To run them, pass the :code:`--runslow` flag
when invoking pytest::

    pytest --runslow


.. _live tests:

Live tests
-----------

Tests that hit live web sites should be marked_ as `webtest`, allowing them to be `executed selectively`_::

    @pytest.mark.webtest
    def test_that_hits_live_website():
        ...

    # On the command line, run only tests marked as "webtest"
    pytest -m webtest

In many cases, tests that hit live websites should be marked as both `webtest` and `slow`::

    @pytest.mark.webtest
    @pytest.mark.slow
    def test_that_hits_live_website():
        ...

    # On the command line, use both flags to target long-running webtests
    pytest --runslow -m webtest

Live web tests of Selenium-based scrapers will open a web browser by default.
All tests of Selenium scrapers should use the :code:`headless` fixture in order to provide
the ability to disable running tests in browser.

These tests should typically be marked as `slow` and `webtest` as well.::

    @pytest.mark.webtest
    @pytest.mark.slow
    def test_selenium_scrape(headless):

You can activate headless mode when running pytest by using the :code:`--headless` flag::

    pytest --headless --runslow


Test login credentials
-----------------------

Tests that hit :ref:`live web sites <live tests>` may require authentication,
as in the case of some Odyssey sites such as Dekalb and Chatham counties
in Georgia.

Such tests require creating user accounts and adding login credentials
to a local YAML :ref:`configuration <configuration>` file.


.. _marked: https://docs.pytest.org/en/stable/example/markers.html
.. _executed selectively: https://docs.pytest.org/en/stable/example/markers.html#marking-test-functions-and-selecting-them-for-a-run
