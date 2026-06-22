.PHONY: help venv install start shell dbshell \
        makemigrations migrate collectstatic \
        createsuperuser test check clean \
	app name=

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
MANAGE := $(PYTHON) manage.py

VENV := .venv

help:
	@echo "Available targets:"
	@echo "  venv             Create virtual environment"
	@echo "  install          Install dependencies"
	@echo "  init             Create venv, install deps & startproject"
	@echo "  app name=x       Create new app"
	@echo "  start            Run development server"
	@echo "  shell            Open Django shell"
	@echo "  dbshell          Open database shell"
	@echo "  makemigrations   Create migrations"
	@echo "  migrate          Apply migrations"
	@echo "  createsuperuser  Create admin user"
	@echo "  collectstatic    Collect static files"
	@echo "  test             Run tests"
	@echo "  check            Run Django checks"
	@echo "  clean            Remove Python cache files"

venv:
	python -m venv $(VENV)

source:
	. .venv/bin/activate

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

init: install
	$(PYTHON) -m django startproject core .

app:
	$(eval APP_NAME := $(word 2, $(MAKECMDGOALS)))
	@if [ -z "$(APP_NAME)" ]; then \
		echo "Usage: make app <name>"; \
		exit 1; \
	fi
	$(MANAGE) startapp $(APP_NAME)

%:
	@:

start:
	$(MANAGE) runserver

shell:
	$(MANAGE) shell

dbshell:
	$(MANAGE) dbshell

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

createsuperuser:
	$(MANAGE) createsuperuser

collectstatic:
	$(MANAGE) collectstatic

test:
	$(MANAGE) test

check:
	$(MANAGE) check

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
