.DEFAULT_GOAL := help


#
# Browser helpers
#

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"


#
# Python helpers
#

PIPENV := pipenv run
PYTHON := $(PYTHON) python -W ignore

define python
    @echo "🐍🤖 $(OBJ_COLOR)Executing Python script $(1)$(NO_COLOR)\r";
    @$(PYTHON) $(1)
endef

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


help:
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


#
# Cleaning
#

## remove all build, test, coverage and Python artifacts
clean: clean-build \
       clean-pyc \
       clean-test


clean-build: ## remove build artifacts
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +


clean-pyc: ## remove Python file artifacts
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +


clean-test: ## remove test and coverage artifacts
	@rm -fr .tox/
	@rm -f .coverage
	@rm -fr htmlcov/


#
# Tests
#

lint: ## check style with flake8
	@$(PIPENV) flake8 court_scraper tests


test: ## run tests quickly with the default Python
	@$(PIPENV) pytest


test-all: ## run tests on every Python version with tox
	@$(PIPENV) tox -p auto


coverage: ## check code coverage quickly with the default Python
	@$(PIPENV) coverage run --source court_scraper -m pytest
	@$(PIPENV) coverage report -m
	@$(PIPENV) coverage html
	@$(BROWSER) htmlcov/index.html


#
# Docs
#

docs: ## generate Sphinx HTML documentation, including API docs
	@rm -f docs/court_scraper.rst
	@rm -f docs/modules.rst
	@$(PIPENV) sphinx-apidoc -o docs/ court_scraper
	@$(PIPENV) $(MAKE) -C docs clean
	@$(PIPENV) $(MAKE) -C docs html
	@$(BROWSER) docs/_build/html/index.html


servedocs: docs ## compile the docs watching for changes
	@$(PIPENV) watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .


#
# Releases
#

check-release: ## check release for potential errors
	@$(PIPENV) twine check dist/*


test-release: clean dist ## release distros to test.pypi.org
	@$(PIPENV) twine upload -r testpypi dist/*


release: clean dist ## package and upload a release
	@$(PIPENV) twine upload -r pypi dist/*


dist: clean ## builds source and wheel package
	@$(PYTHON) setup.py sdist
	@$(PYTHON) setup.py bdist_wheel
	@ls -l dist


#
# Installation
#

install: clean ## install the package to the active Python's site-packages
	@$(PYTHON) setup.py install


# Mark all the commands that don't have a target
.PHONY: clean \
        clean-test \
        clean-pyc \
        clean-build \
        docs \
        help
