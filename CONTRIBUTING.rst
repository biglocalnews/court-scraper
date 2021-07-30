.. highlight:: shell

.. _contributing:

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/biglocalnews/court-scraper/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Do Research
~~~~~~~~~~~

This project involves a fair bit of research, especially with respect to locating
platforms and sites to scrape. Research jobs are great ways to get involved if
you don't write code but still want to pitch in. Anything tagged
with the "research" and "help wanted" labels on GitHub is fair game.

Write Documentation
~~~~~~~~~~~~~~~~~~~

court-scraper could always use more documentation, whether as part of the
official court-scraper docs, in docstrings, or even on the web in blog posts,
articles, and such.

Our `official docs`_ use restructuredText and Sphinx. To contribute documentation:

* Fork and clone this repo
* Create a virtual environment and perform the next steps inside an active venv
* ``pip install -r requirements.txt`` and ``pip install -r requirements-dev.txt``
* Create a branch for your doc updates and start writing!
* Use `make docs` to build docs and/or use `make servedocs` commands to run a
  Sphinx server that displays doc pages and allows easier reloading of pages in browser
* Create a GitHub Pull Request once you're ready to send us your changes

.. _official docs: https://court-scraper.readthedocs.io/en/latest/?badge=latest

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/biglocalnews/court-scraper/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `court-scraper` for local development.

1. Fork the `court-scraper` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/court-scraper.git

3. Install developement dependencies and your local copy of the code 
   into a virtualenv and set up your fork for local development.
   There are numerous ways to create virtual environments in Python. 
   Below uses the venv_ library built into recent Python versions::
    
    # Create a virtual env alongside the court-scraper git repo
    python -m venv court-scraper-env
    
    # Activate the virtual env
    source court-scraper-env/bin/activate

    # Install dev requirements and the Python package into the venv
    cd court-scraper/
    pip install -r requirements-dev.txt
    python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 court_scraper tests
    $ py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

.. _venv: https://docs.python.org/3/library/venv.html

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, please be sure to review the docs 
   and include necessary updates. For example, new classes, methods
   and functions should be documented.
3. The pull request should work for Python version 3.6 or higher. Check
   https://travis-ci.com/github/biglocalnews/court-scraper/pull_requests
   and make sure that the tests pass for all supported Python versions.
