# Package name, read from pyproject.toml so this Makefile is reusable across projects
PACKAGE := $(shell awk -F'"' '/^name = / {print $$2; exit}' pyproject.toml)

# Minimum coverage percentage required for tests to pass
COVERAGE_FAIL = 70

# Run the test suite
test:
	poetry run pytest

# Format the code using Black
format:
	poetry run black .

# Lint the code using Flake8 (compatible with Black's 88-char line length)
# Enforces F401 (unused imports) and F841 (unused variables) with targeted exceptions
lint:
	poetry run flake8 . --max-line-length=88 --extend-ignore=E203,W503 \
		--per-file-ignores="__init__.py:F401 _version.py:F841"

# Run all quality checks: formatting, linting, and tests
check: format lint test

# Run tests with coverage enforcement (terminal output only)
# Tests themselves are excluded from the coverage measurement.
coverage:
	poetry run coverage run --source=$(PACKAGE) --omit="*/tests/*" -m pytest
	poetry run coverage report --fail-under=$(COVERAGE_FAIL)

# Run tests with coverage and produce an HTML report
coverage-html:
	poetry run coverage run --source=$(PACKAGE) --omit="*/tests/*" -m pytest
	poetry run coverage report --fail-under=$(COVERAGE_FAIL)
	poetry run coverage html
	@echo "HTML coverage report generated at htmlcov/index.html"
