.PHONY: format lint type check fix test pre-commit all

# Format code with ruff
format:
	uv run ruff format .

# Check for linting issues
lint:
	uv run ruff check .

# Check types with mypy
type:
	uv run mypy src/

# Auto-fix linting issues
fix:
	uv run ruff check . --fix

# Run all checks (lint + format check + type check)
check:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy src/

# Run tests
test:
	uv run pytest

# Run pre-commit hooks on all files
pre-commit:
	uv run pre-commit run --all-files

# Format and fix all issues
all: fix format
