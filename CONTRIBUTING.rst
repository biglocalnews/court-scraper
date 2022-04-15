.. highlight:: shell

.. _contributing:

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given. There are plenty of ways
to get involved besides writing code. We've listed a few options below, so
take a gander and reach out on Gitter_ if you have questions.

.. _Gitter: https://gitter.im/court-scraper/general?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
.. _reach out: https://gitter.im/court-scraper/general?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

Ways to Contribute
-------------------

Write a scraper
~~~~~~~~~~~~~~~

Don't see a scraper for your state or county? We'd love to have you
write a scraper to help us expand coverage!

Our :ref:`Writing a scraper <writing a scraper>` page is the best place to get started.
It's also a good idea to file a new ticket for the work on our `Issue tracker`_, or claim
the ticket if one already exists. We're happy to talk through strategies for scraping and
integration with the framework, so please do `reach out`_!

Report Bugs
~~~~~~~~~~~

Report bugs on our `Issue tracker`_.

.. _Issue tracker: https://github.com/biglocalnews/court-scraper/issues

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub `Issue tracker`_ for bugs. Anything tagged with "bug"
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
* Use :code:`make docs` to build docs and/or use :code:`make servedocs` commands to run a
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


.. _code contribution bootstrap:

Get Started!
------------

Ready to contribute? Check out our docs on :ref:`Writing a scraper` and :ref:`Testing`, and see
below steps on setting up `court-scraper` for local development.

1. Fork the `court-scraper` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/court-scraper.git

3. Set up a local virtual environment and install dev dependencies
   for local development with Pipenv_::

    cd court-scraper/
    pipenv install --dev

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    # Lint and test for current Python version
    make test
    make lint

    # Run tests for all Python versions
    # (requires setting up and installing all supported Python versions)
    $ tox

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

.. _Pipenv: https://pipenv.pypa.io/en/latest/

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, please be sure to review the docs
   and include necessary updates. For example, new classes, methods
   and functions should be documented.
3. The pull request should work for Python version 3.6 or higher. Check the `Actions tab`_ on GitHub
   and make sure that the tests pass for all supported Python versions.

.. _Actions tab: https://github.com/biglocalnews/court-scraper/actions
