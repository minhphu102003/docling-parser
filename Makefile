# Makefile for docling-parser project

# Variables
PYTHON := python
UV := uv

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install     Install dependencies using uv"
	@echo "  sync        Sync dependencies using uv"
	@echo "  format      Format code with black and isort"
	@echo "  lint        Check code style with flake8"
	@echo "  test        Run tests"
	@echo "  clean       Clean up generated files"
	@echo "  help        Show this help message"

# Install dependencies
.PHONY: install
install:
	$(UV) pip install -e .

# Sync dependencies
.PHONY: sync
sync:
	$(UV) sync

# Format code
.PHONY: format
format:
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

# Lint code
.PHONY: lint
lint:
	$(PYTHON) -m flake8 .

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*~" -delete
	@find . -type f -name ".*~" -delete
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .mypy_cache