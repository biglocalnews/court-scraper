# court-scraper

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)

## Overview

The `court-scraper` package provides a Python library and command-line
tool that help search and download case information from county courts
in the United States.

## Setup

### Pre-reqs

* Python >= 3.7
* (optional) [Pipenv](https://pipenv.pypa.io/en/latest/) is not required, but useful for contributing code

Additionally, scrapers that rely on Selenium require:

* [Google Chrome](https://www.google.com/chrome/) web browser
* [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

Important notes:

- You must ensure that the version of `chromedriver` matches the version of Google Chrome installed on the machine. To check the version on a Desktop installation, open the Chrome browser and enter the following in the address bar: `chrome://settings/help`
- Make sure the `chromedriver` executable is on your system `PATH`.

### Install

```
pip install git+https://github.com/biglocalnews/court-scraper#egg=court-scraper
```

The `court-scraper` command-line tool will store scraped pages,
logs and other files in the `.court-scraper` folder in the
user's home directory. On Linux/Mac, this defaults to `~/.court-scraper`.

You can override the default location by setting the below environment
variable.

```
# E.g., you might place this in ~/.profile on Mac
export COURT_SCRAPER_DIR=/some/other/path/
```

### Configuration

User credentials to log into court sites should
be stored in a YAML configuration file.

This file is expected to live inside the storage
location for scraped files, logs, etc.

On Mac/Linux, it woudl live at `~/.court-scraper/config.yaml`.

The YAML configuration must contain credentials for each
location based on a place ID, which is a combination
of state and county (e.g. `ga_dekalb` for Dekalb County, GA).

Courts with a common software platform that allow sharing
of credentials can inherit credentials from a single entry

Here's an example configuration file:

```
platforms:
  # Mark a platform pass for reuse in multiple sites
  odyssey_site: &ODYSSEY_SITE
      username: 'user@example.com'
      password: 'SECRET_PASS'
# Inherit platform credentials across multiple courts
ga_chatham: *ODYSSEY_SITE
ga_dekalb: *ODYSSEY_SITE
ga_fulton: *ODYSSEY_SITE

# Or simply set site-specific attributes
ny_westchester
  username: 'user2@example.com'
  password: 'GREAT_PASSWORD'
```

## Usage

### Info

The `court-scraper` command-line tool provides information
on the available court sites via the `info` subcommand.

```
> court-scraper info

Available scrapers:

 * GA - Chatham (ga_chatham)
 * GA - Dekalb (ga_dekalb)
 * GA - Fulton (ga_fulton)
```

In the above output, the items in parentheses are
IDs for the state and county.

> You will need these IDs to run a search on a particular court site.

### Search

To search for cases, use the `search` subcommand.

> Note the use of the place ID acquired from the [`info` subcommand](#info).

```
# Search Dekalb County, GA for CASE ID 123
court-scraper search --place-id ga_dekalb ---search-term 123

```

You can also supply a text file containing a list of search terms
-- one term per line -- to the `search` command.

```
# Search a series of terms in Dekalb County, GA
court-scraper search \
  --place-id ga_dekalb \
  --search-terms-file ga_dekalb_terms.txt
```

If a scraper uses Selenium, you can choose to launch a browser with the
`--with-browser` flag:

```
court-scraper search \
  --place-id ga_dekalb \
  --search-term 123 \
  --with-browser
```

### Data and files

Scrapers will generally store raw file assets (e.g. HTML pages, CSV file) for
case details in a local cache. They will also store basic case metadata such
as court location, case number, and filing date in a SQLite database.

```
# A search for two case IDs for Dekalb County, GA

> court-scraper search -p ga_dekalb -f ga_dekalb_search_terms.txt
Executing search for ga_dekalb
Caching file: /Users/someuser/.court-scraper/cache/ga_dekalb/19D67383.html
Caching file: /Users/someuser/.court-scraper/cache/ga_dekalb/19D102716.html
Adding 2 results to /Users/someuser/.court-scraper/cases.db
```

## Contributing

### Overview

We welcome contributions of new court scrapers as well as bug fixes.

It's generally a good idea to review our [Issues][] and start a conversation
with our team before implementing code, to ensure the code meets our standards
and to avoid duplication of effort.

[Issues]: https://github.com/biglocalnews/court-scraper/issues

To send us code:

* Fork this repo
* Add a site scraper using the [steps outlined below](#adding-a-scraper)
* Send us a pull request

> Please try to include test coverage for contributions, and
> ensure that existing test coverage passes before sending a pull
> request. Pull requests will not be accepted for code that breaks
> existing functionality.

### Adding a scraper

The main task involved in contributing a scraper involves creating a
a "site" class that provides generic search functionality.

In concrete terms, this means adding a site class with a `search`
method and a `login` method, if users are required to log into a site.

The code for a given court will vary widely in terms of complexity, so
we don't place stringent requirements on the overall structure of code
contributions. However, we do require that you provide a standard public
interface to a given site through a `search` method.

Here's an incredibly simplified example of a potential scraper for
Westchester County, NY:

```
# court_scraper/scrapers/ny_westchester.py

class NyWestchester:

    def __init__(self, url, download_dir):
        self.site_url = url
        self.download_dir = download_dir

    def search(self, search_terms=[], =True):
        # Do things of varying complexity with search terms.
        # This method should return a list of CaseInfo
        # instances containing case metadata and, if available,
        # HTML for case detail
        pass
```

A scraper specific to a single county/court should live in
the `court_scraper.scrapers` namespace in modules named by state and county.

For example, the example class for Westchester County would live in
 `court_scraper/scrapers/ny_westchester.py`.

> Note that we use CamelCase names for the classes!!

Many counties use common software platforms, such as Odyssey by
Tyler Technologies, to provide case information.

To add a platform-based scraper for use in more than one jurisdiction,
add a site class to the `court_scraper.platforms` namespace.

For example, `court_scraper/platforms/odyssey_site.py`.

The final step to adding a site scraper involves adding some
metadata to [sites_meta.csv][]. This file contains
the following fields:

[sites_meta.csv]: https://github.com/biglocalnews/court-scraper/blob/master/court_scraper/data/sites_meta.csv

* `state` - 2-letter state abbreviation, lower cased
* `county` - Name of county (without the word "County"), lower cased
* `site_type` - Base name of the Python module where the scraper lives.
   For For example, `ny_westchester` for single-location sites; `odyssey_site` for platform-based sites.
* `site_version` - Platform based sites often have multiple versions.
  Use this field to denote a new version of a platform-based site.
* `captcha_service_required` - Mark an "x" in this field if a site uses
  Captchas
* `home_url` - Starting page for a site scraper

It's important to note that *every jurisdiction covered* by a site scraper
must be entered in `sites_meta.csv`, even if the sites share a common
platform. For example, there are separate entries in `sites_meta.csv`
for Chatham, Dekalb and Fulton counties in Georgia, even though all
three sites use the same version of the Odyssey courts platform.
