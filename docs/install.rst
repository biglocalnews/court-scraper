.. _install:

Installation
============

Install
-------

.. code::

   pip install court-scraper

Upon installation, you should have access to the :code:`court-scraper` tool on the command line. Use the
:code:`--help` flag to view available sub-commands::

  court-scraper --help


You should also be able to import the :code:`court_scraper` package from a Python script.::


  import court_scraper
  print(court_scraper.__version__)

.. note:: See :ref:`the usage docs <usage>` for details on using *court-scraper* on
  the command line and in custom scripts.


.. _default cache dir:

Default cache directory
-------------------------

By default, files downloaded by the command-line tool will be saved to the :code:`.court-scraper` folder
in the user's home directory.

On Linux/Mac systems, this will be :code:`~/.court-scraper/`.


.. _customize cache dir:

Customize cache directory
-------------------------

To use an alternate cache directory, set the below environment variable
(e.g. in a :code:`~/.bashrc` or :code:`~/.bash_profile` configuration file)::

   export COURT_SCRAPER_DIR=/tmp/some_other_dir


.. _configuration:

Configuration
-------------

Many court sites require user credentials to log in or present
:ref:`CAPTCHAs <captcha sites>` that must be handled
using a paid, third-party service (`court-scraper` uses `Anti-captcha`_).

Sensitive information such as user logins and the API key
for a CAPTCHA service should be stored in a YAML configuration file called `config.yaml`.

This file is expected to live inside the :ref:`default storage location <default cache dir>`
for scraped files, logs, etc.

On Linux/Mac, the default location is :code:`~/.court-scraper/config.yaml`.

This configuration file must contain credentials for each
location based on a :ref:`Place ID <place id>`, which is a `snake_case <https://en.wikipedia.org/wiki/Snake_case>`_
combination of state and county (e.g. `ga_dekalb` for Dekalb County, GA).

Courts with a common software platform that allow sharing
of credentials can inherit credentials from a single entry.

Here's an example configuration file::

  # ~/.court-scraper/config.yaml
  captcha_service_api_key: 'YOUR_ANTICAPTCHA_KEY'
  platforms:
    # Mark a platform user/pass for reuse in multiple sites
    odyssey_site: &ODYSSEY_SITE
      username: 'user@example.com'
      password: 'SECRET_PASS'
  # Inherit platform credentials across multiple courts
  ga_chatham: *ODYSSEY_SITE
  ga_dekalb: *ODYSSEY_SITE
  ga_fulton: *ODYSSEY_SITE

  # Or simply set site-specific attributes
  ny_westchester:
    username: 'user2@example.com'
    password: 'GREAT_PASSWORD'


.. _captcha sites:

CAPTCHA-protected sites
~~~~~~~~~~~~~~~~~~~~~~~

`court-scraper` uses the `Anti-captcha`_ service to handle sites
protected by CAPTCHAs_.

.. _Anti-captcha: https://anti-captcha.com
.. _CAPTCHAS: https://en.wikipedia.org/wiki/CAPTCHA

If you plan to scrape a CAPTCHA-protected site, register with the
`Anti-captcha`_ service and obtain an API key.

Then, add your API key to your local court-scraper configuration file as shown below::


  # ~/.court-scraper/config.yaml
  captcha_service_api_key: 'YOUR_API_KEY'

Once configured, you should be able to query CAPTCHA-protected sites currently supported by `court-scraper`.
