.PHONY: install test lint format check

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check app

format:
	ruff format app
	ruff check app --fix

check: lint test