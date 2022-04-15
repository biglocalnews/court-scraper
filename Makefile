.DEFAULT_GOAL := help

#
# Colors
#

# Define ANSI color codes
RESET_COLOR   = \033[m

BLUE       = \033[1;34m
YELLOW     = \033[1;33m
GREEN      = \033[1;32m
RED        = \033[1;31m
BLACK      = \033[1;30m
MAGENTA    = \033[1;35m
CYAN       = \033[1;36m
WHITE      = \033[1;37m

DBLUE      = \033[0;34m
DYELLOW    = \033[0;33m
DGREEN     = \033[0;32m
DRED       = \033[0;31m
DBLACK     = \033[0;30m
DMAGENTA   = \033[0;35m
DCYAN      = \033[0;36m
DWHITE     = \033[0;37m

BG_WHITE   = \033[47m
BG_RED     = \033[41m
BG_GREEN   = \033[42m
BG_YELLOW  = \033[43m
BG_BLUE    = \033[44m
BG_MAGENTA = \033[45m
BG_CYAN    = \033[46m

# Name some of the colors
COM_COLOR   = $(DBLUE)
OBJ_COLOR   = $(DCYAN)
OK_COLOR    = $(DGREEN)
ERROR_COLOR = $(DRED)
WARN_COLOR  = $(DYELLOW)
NO_COLOR    = $(RESET_COLOR)

OK_STRING    = "[OK]"
ERROR_STRING = "[ERROR]"
WARN_STRING  = "[WARNING]"

define banner
    @echo "  $(BLUE)__________$(RESET_COLOR)"
    @echo "$(BLUE) |$(RED)BIG🌲LOCAL$(RESET_COLOR)$(BLUE)|$(RESET_COLOR)"
    @echo "$(BLUE) |&&& ======|$(RESET_COLOR)"
    @echo "$(BLUE) |=== ======|$(RESET_COLOR)  $(DWHITE)This is a $(RESET_COLOR)$(BG_RED)$(WHITE)Big Local News$(RESET_COLOR)$(DWHITE) automation$(RESET_COLOR)"
    @echo "$(BLUE) |=== == %%%|$(RESET_COLOR)"
    @echo "$(BLUE) |[_] ======|$(RESET_COLOR)  $(1)"
    @echo "$(BLUE) |=== ===!##|$(RESET_COLOR)"
    @echo "$(BLUE) |__________|$(RESET_COLOR)"
    @echo ""
endef


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
PYTEST := $(PIPENV) py.test

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
# Tests
#

lint: ## run the linter
	$(call banner,        💅 Linting code 💅)
	@$(PIPENV) flake8 ./


test: ## run all quick tests with the default Python
	@$(PYTEST)


test-slow: ## run all slow tests
	@$(PYTEST) --runslow


test-slow-nocaptcha: ## run only slow tests that do not require captcha
	@$(PYTEST) --runslow -m nocaptcha


test-slow-captcha: ## run only slow tests that do not require captcha
	@$(PYTEST) --runslow -m captcha


coverage: ## check code coverage quickly with the default Python
	@$(PIPENV) coverage run --source court_scraper -m pytest
	@$(PIPENV) coverage report -m
	@$(PIPENV) coverage html
	@$(BROWSER) htmlcov/index.html


#
# Docs
#

serve-docs: ## start the documentation test server
	$(call banner,         📃 Serving docs 📃)
	cd docs && $(PIPENV) make livehtml;


test-docs: ## build the docs as html
	$(call banner,        📃 Building docs 📃)
	cd docs && $(PIPENV) make html;


#
# Releases
#

check-release: ## check release for potential errors
	$(call banner,      🔎 Checking release 🔎)
	@$(PIPENV) twine check dist/*


build-release: ## builds source and wheel package
	$(call banner,      📦 Building release 📦)
	@$(PYTHON) setup.py sdist
	@ls -l dist



# Mark all the commands that don't have a target
.PHONY: help \
        lint \
        test \
        test-slow \
        test-slow-nocaptcha \
        test-slow-captcha \
        coverage \
        test-docs \
        serve-docs \
        check-release
