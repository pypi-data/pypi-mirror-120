.PHONY: clean clean-test clean-pyc clean-build docs help coverage
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"
PACKAGE_NAME = "power_cogs"


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr coverage/
	rm -fr .pytest_cache

lint: ## check style with flake8
	isort --profile black $(PACKAGE_NAME) tests
	black $(PACKAGE_NAME) tests
	flake8 $(PACKAGE_NAME) tests

test-no-html: ## run tests quickly with the default Python
	pytest tests/

test:
	pytest --html=html/report.html tests/
	$(BROWSER) html/report.html

test-all: ## run tests on every Python version with tox
	tox

coverage:	## code coverage xml
	pytest --cov-report term --cov=$(PACKAGE_NAME)/
	pytest --cov-report xml:coverage/coverage.xml --cov=$(PACKAGE_NAME)/

coverage-html:	## code coverage html
	pytest --cov-report term --cov=$(PACKAGE_NAME)/
	pytest --cov-report html:coverage/html --cov=$(PACKAGE_NAME)/
	$(BROWSER) coverage/html/index.html


docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/$(PACKAGE_NAME).rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ $(PACKAGE_NAME)
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean lint ## install the package to the active Python's site-packages
	python setup.py install

commit: lint install test docs
	git add .
	git commit -a

push:
	make lint
	git add .
	git commit
	git push origin HEAD

unsafe-push:
	git add .
	git commit
	git push origin HEAD
