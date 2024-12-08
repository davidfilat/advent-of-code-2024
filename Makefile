PYTHON := pypy

export PYTHONPATH := src:$(PYTHONPATH)

VENV := .venv
VENV_ACTIVATE := $(VENV)/bin/activate
.PHONY: all venv lint format clean run

all: venv lint format

venv:
	uv venv $(VENV)
	uv install

lint:
	uv run ruff check src tests

format:
	uv run ruff format src

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

run:
	@if [ -z "$(day)" ]; then \
		echo "Usage: make run day=<day_number>"; \
		exit 1; \
	fi; \
	uv run python src/day$${day}.py

help:
	@echo "Available targets:"
	@echo "  all     : Set up virtual environment, lint, and format"
	@echo "  venv    : Create virtual environment and install dependencies using uv"
	@echo "  lint    : Run ruff linter"
	@echo "  format  : Format code using ruff"
	@echo "  clean   : Clean up virtual environment and cache files"
	@echo "  run     : Run a specific day's script (usage: make run day=<day_number>)"
	@echo "  help    : Show this help message"

%:
	@: