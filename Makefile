.PHONY: install test lint format check

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src

format:
	ruff format src
	ruff check src --fix

check: lint test