set shell := ["bash", "-uc"]

init-venv:
	rm -rf .venv 2> /dev/null
	python3 -m venv .venv
	.venv/bin/pip install -q pip-tools

compile-deps:
	.venv/bin/pip-compile -q --resolver=backtracking req/requirements.in --strip-extras

compile-deps-dev:
	.venv/bin/pip-compile -q -o requirements-dev.txt --resolver=backtracking req/requirements-dev.in --strip-extras

compile-all-deps: compile-deps compile-deps-dev

install-deps:
	.venv/bin/pip-sync -q requirements.txt

install-dev-deps:
	.venv/bin/pip-sync -q requirements-dev.txt

install-all-deps:
	.venv/bin/pip-sync -q requirements-dev.txt requirements.txt

compile-and-install-all-deps: compile-all-deps install-all-deps

lint:
	.venv/bin/black . --exclude=.venv
	.venv/bin/isort . --skip .venv   
	.venv/bin/flake8 . --exclude .venv

mdlint:
	.venv/bin/pymarkdown scan .

run:
	.venv/bin/python3 main.py

